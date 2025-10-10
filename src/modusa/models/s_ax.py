#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import immutable_property, validate_args_type
from .base import ModusaSignalAxis
from .data import Data
from modusa.tools.math_ops import MathOps
from typing import Self, Any, Callable
import numpy as np
import matplotlib.pyplot as plt

class SAx(ModusaSignalAxis):
	"""
	Space to represent any signal's axis.

	Parameters
	----------
	values: array-like
		- Any array-like object on which np.asarray can be applied.
	label: str
		- Label for the axis.
		- Default: None => ''

	Note
	----
	- Use :class:`~modusa.generators.s_ax.SAxGen` API to instantiate this class.
	- It can be uniform/non-uniform.
	- It is numpy compatible, so you can use numpy methods directly on this class object.
	- Since the object of this class represents an axis, any mathematical operations on it will result in another object of :class:`~modusa.models.s1d.S1D` class with `y` being the result of the operation and `x` being the axis itself.
	"""
	
	#--------Meta Information----------
	_name = "Signal Axis"
	_nickname = "axis" # This is to be used in repr/str methods
	_description = "Axis for different types of signals."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-20"
	#----------------------------------
	
	@validate_args_type()
	def __init__(self, values, label = None):
		
		super().__init__() # Instantiating `ModusaSignalAxis` class

		values = np.asarray(values)
		if values.ndim == 0:
			values = np.asarray([values])
		
		assert values.ndim == 1
	
		self._values = values
		self._label = label or ""
	
	#-----------------------------------
	# Properties (User Facing)
	#-----------------------------------
	
	@property
	def values(self) -> np.ndarray:
		return self._values
	
	@property
	def label(self) -> str:
		return self._label
		
	@property
	def shape(self) -> tuple:
		return self.values.shape
	
	@property
	def ndim(self) -> int:
		return self.values.ndim # Should be 1
	
	@property
	def size(self) -> int:
		return self.values.size
	
	#====================================
	
	#------------------------------------
	# Utility methods
	#------------------------------------
	
	def is_same_as(self, other) -> bool:
		"""
		Compare it with another SAx object.

		Parameters
		----------
		other: SAx
			Another object to compare with.
		
		Returns
		-------
		bool
			True if same ow False

		Note
		----
		- We check the shape and all the values.
		- We are not checking the labels for now.
		"""
		
		if other.size == 1: # Meaning it is scalar
			return True
		
		axis1_arr = np.asarray(self)
		axis2_arr = np.asarray(other)
		
		if not isinstance(axis2_arr, type(axis1_arr)):
			return False
		if axis1_arr.shape != axis2_arr.shape:
			return False
		if not np.allclose(axis1_arr, axis2_arr):
			return False
		
		return True
	
	def copy(self) -> Self:
		"""
		Return a new copy of SAx object.
		
		Returns
		-------
		SAx
			A new copy of the SAx object.
		"""
		copied_values = np.asarray(self).copy()
		copied_label = self.label
		
		return self.__class__(values=copied_values, label=copied_label)
	
	def set_meta_info(self, label):
		"""
		Set meta info for the axis.
		
		.. code-block:: python
		
			import modusa as ms
			x = ms.sax.linear(100, 10)
			print(x)
			x = x.set_meta_info("My Axis (unit)")
			print(x)

			# I personally prefer setting it inline
			x = ms.sax.linear(100, 10).set_meta_info("My Axis (unit)")
			print(x)
		
		Parameters
		----------
		label: str
			Label for the axis (e.g. "Time (sec)").
		Returns
		-------
		Self
			A new Self instance with new label.
		"""
		
		if label is None:
			return self
		else:
			return self.__class__(values=self.values.copy(), label=label)
		
	
	def index_of(self, value) -> int:
		"""
		Return the index whose value is closest
		to `value`.

		Parameters
		----------
		value: float
			value to find the index of.
		
		Returns
		-------
		int
			Index with value closest to the `value`
		"""
		from .data import Data
		
		idx = np.argmin(np.abs(self.values - value))
		
		return Data(values=idx, label=None)

	#====================================
	
	#-------------------------------
	# NumPy Protocol
	#-------------------------------
	
	def __array__(self, dtype=None) -> np.ndarray:
		return np.asarray(self.values, dtype=dtype)
	
	def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
		"""
		Provides operation support for the universal functions
		on the Data object.
		"""
		from .s1d import S1D
		from .data import Data
		
		raw_inputs = [x.values if isinstance(x, type(self)) else x for x in inputs]
		
		# Call the actual ufunc
		result = getattr(ufunc, method)(*raw_inputs, **kwargs)
		
		if isinstance(result, (np.ndarray, np.generic)):
			y = Data(values=result, label=None)
			x = self
			return S1D(y=y, x=x, title=None)
		else:
			return result
		
	def __array_function__(self, func, types, args, kwargs):
		"""
		Additional numpy function support.
		"""
		from modusa.utils import np_func_cat as nfc
		from .data import Data
		
		if not all(issubclass(t, type(self)) for t in types):
			return NotImplemented
		
		# Not supporting concatenate like operations as axis any random axis can't be concatenated
		if func in nfc.CONCAT_FUNCS:
			raise NotImplementedError(f"`{func.__name__}` is not yet tested on modusa signal, please create a GitHub issue.")
			
		# Single signal input expected
		x = args[0]
		x_arr = np.asarray(x)
		result = func(x_arr, **kwargs)
		
		if func in nfc.REDUCTION_FUNCS:
			# If the number of dimensions is reduced
			if result.ndim == 0:
				return Data(values=result, label=None)
			else:
				raise RuntimeError(f"Unexpected result: `result` has more than 0 dimensions, {result.ndim}")
				
		elif func in nfc.X_NEEDS_ADJUSTMENT_FUNCS:
			# You must define logic for adjusting x
			raise NotImplementedError(f"{func.__name__} requires x-axis adjustment logic.")
			
		else:
			raise NotImplementedError(f"`{func.__name__}` is not yet tested on modusa signal, please create a GitHub issue.")
	
	#================================
	
	
	#------------------------------------
	# Visualisation
	#------------------------------------
	
	def plot(self, ax = None, fmt = "b-", show_stem=False):
		"""
		Plot the axis values. This is useful to analyse
		the axis if it is linear or follows some other
		trend.

		.. code-block:: python
			
			import modusa as ms
			x = ms.sax.linear(100, 10)
			x.plot()

		Parameters
		----------
		ax: plt.Axes | None
			- Incase, you want to plot it on your defined matplot ax.
			- If not provided, We create a new figure and return that.
		fmt: str
			- Matplotlib fmt for setting different colors and styles for the plot.
			- General fmt is [color][marker][line], e.g. "bo:"
			- Useful while plotting multiple SAx instances on the same plot.

		Returns
		-------
		plt.Figure | None
			- Figure if ax is None.
			- None is ax is not None.
		"""
		from modusa.tools.plotter import Plotter
		
		fig: plt.Figure | None = Plotter.plot_signal(y=self.values, x=np.arange(len(self)), ax=ax, fmt=fmt, title=self.label, y_label=self.label, x_label="Index", show_stem=show_stem)
		
		return fig
	#====================================
	
	#-----------------------------------
	# Indexing
	#-----------------------------------
	
	def __getitem__(self, key) -> Self:
		"""
		Defining how to index SAx instance.

		.. code-block:: python
			
			import modusa as ms
			x = ms.sax.linear(100, 10)
			print(x)
			print(x[10:20])

		Parameters
		----------
		key: int | slice
			What can go inside the square bracket [] for indexing.
		
		Returns
		-------
		SAx:
			Sliced instance of the axis.
		"""
		
		from .s1d import S1D
		
		if not isinstance(key, (int, slice, tuple)):
			raise TypeError(f"Invalid key type {type(key)}")
	
		sliced_values = self.values[key]
		
		# If the number of dimensions is reduced, add back singleton dims
		while np.ndim(sliced_values) < self.ndim:
			sliced_values = np.expand_dims(sliced_values, axis=0)
		
		return self.__class__(values=sliced_values, label=self.label)
	
	
	def __setitem__(self, key, value):
		"""
		Raises error if trying to set values
		of an axis.

		Meaningful axis are not meant to be altered.
		"""
		raise TypeError("Axis do not support item assignment.")

	#===============================
	
	#-------------------------------
	# Basic arithmetic operations
	#-------------------------------
	def __add__(self, other):
		return np.add(self, other) 
	
	def __radd__(self, other):
		return np.add(other, self)
	
	def __sub__(self, other):
		return np.subtract(self, other)
	
	def __rsub__(self, other):
		return np.subtract(other, self)
	
	def __mul__(self, other):
		return np.multiply(self, other) 
	
	def __rmul__(self, other):
		return np.multiply(other, self)
	
	def __truediv__(self, other):
		return np.divide(self, other) 
	
	def __rtruediv__(self, other):
		return np.divide(other, self)
	
	def __floordiv__(self, other):
		return np.floor_divide(self, other) 
	
	def __rfloordiv__(self, other):
		return np.floor_divide(other, self)
	
	def __pow__(self, other):
		return np.power(self, other) 
	
	def __rpow__(self, other):
		return np.power(other, self)
	
	#===============================
	
	
	#-------------------------------
	# Basic comparison operations
	#-------------------------------
	def __eq__(self, other):
		return np.equal(self, other)
	
	def __ne__(self, other):
		return np.not_equal(self, other)
	
	def __lt__(self, other):
		return np.less(self, other)
	
	def __le__(self, other):
		return np.less_equal(self, other)
	
	def __gt__(self, other):
		return np.greater(self, other)
	
	def __ge__(self, other):
		return np.greater_equal(self, other)
	
	#===============================

	#----------------------------------
	# Information
	#----------------------------------
	
	def print_info(self) -> None:
		"""
		Prints info about the SAx instance.
		
		.. code-block:: python
			
			import modusa as ms
			# For SAx
			x = ms.sax.linear(100, 10)
			x.print_info()
			# For TAx
			x = ms.tax.linear(100, 10)
			x.print_info()
		
		Returns
		-------
		None
		"""
		print("-" * 50)
		print("Axis Info")
		print("-" * 50)
		print(f"{'Label':<20}: {self.label}")
		print(f"{'Shape':<20}: {self.shape}")
		# Inheritance chain
		cls_chain = " → ".join(cls.__name__ for cls in reversed(self.__class__.__mro__[:-1]))
		print(f"{'Inheritance':<20}: {cls_chain}")
		print("=" * 50)
	
	def __str__(self):
		arr_str = np.array2string(self.values, separator=", ", threshold=30, edgeitems=3, max_line_width=120)
		return f"{self._nickname}({arr_str})"
	
	def __repr__(self):
		arr_str = np.array2string(self.values, separator=", ", threshold=30, edgeitems=3, max_line_width=120)
		return f"{self._nickname}({arr_str})"
	#===================================
	