#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import immutable_property, validate_args_type
from .s_ax import SAx
from typing import Self, Any, Callable
import numpy as np

class TAx(SAx):
	"""
	A Space to represent time axis.

	Note
	----
	- Use :class:`~modusa.generators.t_ax.TAxGen` API to instantiate this class.
	- It must be uniform with a well-defined sampling rate.
	- You are likely to be using this axis for most of the cases.
	- It is numpy compatible, so you can use numpy methods directly on this class object.
	- Since the object of this class represents time axis, any mathematical operations on it will result in another object of :class:`~modusa.models.tds.TDS` class with `y` being the result of the operation and `t` being the axis itself.
	
	Parameters
	----------
	n_points: int
		- Number of data points for the time axis.
	sr: float
		- Sampling rate.
		- Default: 1.0
	t0: float
		- Start timestamp.
		- Default: 0.0
	label: str
		- Label associated with the time axis.
		- Default: None => ''
		- e.g. (Time (sec))
	"""
	
	#--------Meta Information----------
	_name = "Time Axis"
	_nickname = "axis" # This is to be used in repr/str methods
	_description = "A Space to represent time axis."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-26"
	#----------------------------------
	
	@validate_args_type()
	def __init__(self, n_points, sr=1.0, t0=0.0, label=None):
		
		# Create `t` time series array
		t = t0 + np.arange(n_points) / sr
		
		super().__init__(values=t, label=label) # Instantiating `SAx` class
		
		# Storing other parameters so that we can use them.
		self._sr = sr
		self._t0 = t0
		

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
	
	@property
	def sr(self) -> float:
		return self._sr
	
	@property
	def t0(self) -> float:
		return self._t0
	
	@property
	def end_time(self) -> float:
		return float(self.values[-1])
	
	@property
	def duration(self) -> float:
		return float(self.end_time - self.t0)
	
	def __len__(self) -> int:
		return len(self.values)
	
	#===================================
	
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
		
		return self.__class__(n_points=self.shape[0], sr=self.sr, t0=self.t0, label=self.label)
	
	
	def set_meta_info(self, label):
		"""
		Set meta info for the axis.

		Parameters
		----------
		label: str
			Label for the axis (e.g. "Time (sec)").
		Returns
		-------
		Self
			A new Self instance with new label.
		
		.. code-block:: python
		
			import modusa as ms
			x = ms.sax.linear(100, 10)
			print(x)
			x = x.set_meta_info("My Axis (unit)")
			print(x)

			# I personally prefer setting it inline
			x = ms.sax.linear(100, 10).set_meta_info("My Axis (unit)")
			print(x)
		
		"""
		
		if label is None:
			return self
		else:
			return self.__class__(n_points=self.shape[0], sr=self.sr, t0=self.t0, label=label)
		
	def translate(self, n_samples):
		"""
		Translate the time axis by `n_samples`.

		Note
		----
		- `n_samples` can be both positive and negative.
		- You might end up getting -ve time values as we are not checking for the values rn.

		Parameters
		----------
		n_samples: int
			- Number of samples to move the signal.
			- +ve => moving signal forward.
			- -ve => moving signal backward.
		
		Returns
		-------
		TAx
			Translated axis.
		"""
		
		new_t0 = self.t0 + (n_samples / self.sr)
		
		return self.__class__(n_points=self.shape[0], sr=self.sr, t0=new_t0, label=self.label)
	
	#===================================
	
	
	#-------------------------------
	# NumPy Protocol
	#-------------------------------
	def __array__(self, dtype=None) -> np.ndarray:
		return np.asarray(self.values, dtype=dtype)
	
	def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
		"""
		Provides operation support for the universal functions
		on the TAx object.
		"""
		from .tds import TDS
		from .data import Data
		
		raw_inputs = [t.values if isinstance(t, type(self)) else t for t in inputs]
		
		# Call the actual ufunc
		result = getattr(ufunc, method)(*raw_inputs, **kwargs)
		
		if isinstance(result, (np.ndarray, np.generic)):
			y = Data(values=result, label=None)
			t = self
			return TDS(y=y, t=t, title=None)
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
		t = args[0]
		t_arr = np.asarray(t)
		result = func(t_arr, **kwargs)
		
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
		if not isinstance(key, (int, slice, tuple)):
			raise TypeError(f"Invalid key type {type(key)}")
		
		if isinstance(key, int):
			sliced_value = self.values[key]
			new_t0 = sliced_value
			return self.__class__(n_points=1, sr=self.sr, t0=new_t0, label=self.label)
			
		elif isinstance(key, slice):
			step = key.step or 1
			if step < 0:
				raise ValueError("Reversed slicing of time axis is not allowed.")
	
			sliced_values = self.values[key]
			new_n_points = len(sliced_values)
			new_sr = self.sr / step
			new_t0 = sliced_values[0]
		
			return self.__class__(n_points=new_n_points, sr=new_sr, t0=new_t0, label=self.label)
	
	
	def __setitem__(self, key, value):
		"""
		Raises error if trying to set values
		of an axis.

		Meaningful axis are not meant to be altered.
		"""
		raise TypeError("Time axis does not support item assignment.")
		
	#===============================