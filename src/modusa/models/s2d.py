#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import immutable_property, validate_args_type
from .base import ModusaSignal
from .s_ax import SAx
from .data import Data
from modusa.tools.math_ops import MathOps
from typing import Self, Any, Callable
from types import NoneType
import numpy as np
import matplotlib.pyplot as plt
import copy

class S2D(ModusaSignal):
	"""
	Space to represent 2D signal.

	Note
	----
	- Use :class:`~modusa.generators.s2d.S2DGen` API to instantiate this class.
	- The signal can have uniform/non-uniform axes.

	Parameters
	----------
	M: Data
		- Data object holding the main 2D array.
	y: SAx
		- Y-axis of the signal.
	x: SAx
		- X-axis of the signal.
	title: str
		- What does the signal represent?
		- e.g. "MySignal"
		- This is used as the title while plotting.
	"""
	
	#--------Meta Information----------
	_name = "Signal 2D"
	_nickname = "signal" # This is to be used in repr/str methods
	_description = "Space to represent 2D signal."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-20"
	#----------------------------------
	
	def __init__(self, M, y, x, title = None):
		super().__init__() # Instantiating `ModusaSignal` class
		
		if not (isinstance(M, Data) and isinstance(y, SAx), isinstance(x, SAx)):
			raise TypeError(f"`M` must be `Data` instance, `y` and `x` must be `SAx` instances, got {type(M)}, {type(y)} and {type(x)}")
			
		assert M.ndim == 2
		assert M.shape[0] == y.shape[0], f"M and y shape mismatch"
		assert M.shape[1] == x.shape[0], f"M and x shape mismatch"
		
		# All these are private and we do not expose it to users directly.
		self._M = M
		self._y = y
		self._x = x
		self._title = title or self._name
		
	#--------------------------------------
	# Properties
	#--------------------------------------
		
	@property
	def M(self) -> Data:
		return self._M
	
	@property
	def y(self) -> SAx:
		return self._y
	
	@property
	def x(self) -> SAx:
		return self._x
	
	@property
	def title(self) -> str:
		return self._title
	
	@property
	def shape(self) -> tuple:
		return self.M.shape
	
	@property
	def ndim(self) -> tuple:
		return self.M.ndim # Should be 2
	
	@property
	def size(self) -> int:
		return self.M.size
	
	#===============================
	
	
	#-------------------------------
	# NumPy Protocol
	#-------------------------------
	
	def __array__(self, dtype=None) -> np.ndarray:
		return np.asarray(self.M.values, dtype=dtype)
	
	def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
		"""
		Supports NumPy universal functions on the Signal1D object.
		"""
		from .data import Data  # Ensure this is the same Data class you're using
		from modusa.utils import np_func_cat as nfc
		
		raw_inputs = [
			np.asarray(obj.M) if isinstance(obj, type(self)) else obj
			for obj in inputs
		]
		
		result = getattr(ufunc, method)(*raw_inputs, **kwargs)
		
		result = Data(values=result, label=None)
		y = self.y.copy()
		x = self.x.copy()
		
		if result.shape[0] != y.shape[0] or result.shape[1] != x.shape[0]:
			raise ValueError(f"`{ufunc.__name__}` caused shape mismatch between data and axis, please create a github issue")
			
		return self.__class__(M=result, y=y, x=x, title=self.title)
	
	def __array_function__(self, func, types, args, kwargs):
		"""
		Additional numpy function support for modusa signals.
		Handles reduction and ufunc-like behavior.
		"""
		from .data import Data
		from modusa.utils import np_func_cat as nfc
		
		if not all(issubclass(t, type(self)) for t in types):
			return NotImplemented
		
		if func in nfc.CONCAT_FUNCS:
			raise NotImplementedError(f"`{func.__name__}` is not yet tested on modusa signal, please create a GitHub issue.")
			
		signal = args[0]
		result: Data = func(signal.M, **kwargs)
		axis = kwargs.get("axis", None)
		keepdims = kwargs.get("keepdims", None)

		if func in nfc.REDUCTION_FUNCS:
			if keepdims is None or keepdims is True:
				if axis is None: # Both axes collapsed
					dummy_y = SAx(0, label=None)
					dummy_x = SAx(values=0, label=None)
					return self.__class__(M=result, y=dummy_y, x=dummy_x, title=signal.title)
				
				if isinstance(axis, int): # One of the axis collapsed
					if axis == 0:
						dummy_y = SAx(0, label=None)
						return self.__class__(M=result, y=dummy_y, x=signal.x.copy(), title=signal.title)
					elif axis in [1, -1]:
						dummy_x = SAx(values=0, label=None)
						return self.__class__(M=result, y=signal.y.copy(), x=dummy_x, title=signal.title)
					else:
						raise ValueError
			elif keepdims is False:
				if axis is None: # Return Data
					return result
				if axis == 0: # Return S1D
					from .s1d import S1D
					return S1D(y=result, x=signal.x, title=signal.title)
				elif axis in [1, -1]: # Return S1D
					from .s1d import S1D
					return S1D(y=result, x=signal.y, title=signal.title)
				else:
					raise ValueError
				
		elif func in nfc.X_NEEDS_ADJUSTMENT_FUNCS:
			raise NotImplementedError(f"{func.__name__} requires x-axis adjustment logic.")
			
		else:
			raise NotImplementedError(f"`{func.__name__}` is not yet tested on modusa signal, please create a GitHub issue.")
			
			
	#================================
			
	#-------------------------------
	# Indexing
	#-------------------------------
			
	def __getitem__(self, key):
		"""
		Return a sliced or indexed view of the data.
		
		Parameters
		----------
		key : int | slice | S2D
			- Index to apply to the values.
		
		Returns
		-------
		S2D
			- Another sliced S2D object 
		"""
		
		if not isinstance(key, (int, slice, tuple)):
			raise TypeError(f"Invalid key type {type(key)}")
		
		# We slice the data
		sliced_M = self.M[key]
		
		if isinstance(key, (int, slice)):
			sliced_y = self.y[key]
			sliced_x = self.x
		
		if isinstance(key, tuple):
			sliced_y = self.y[key[0]]
			sliced_x = self.x[key[1]]
		
		return self.__class__(M=sliced_M, y=sliced_y, x=sliced_x, title=self.title)
	
		
	
	def __setitem__(self, key, value):
		"""
		Set values at the specified index.
	
		Parameters
		----------
		key : int | slice | array-like | boolean array | S1D
			Index to apply to the values.
		value : int | float | array-like
			Value(s) to set.
		"""
		
		self.M[key] = value  # In-place assignment
		
	#===================================
		
	#-------------------------------
	# Basic arithmetic operations
	#-------------------------------
	def __add__(self, other):
		if isinstance(other, type(self)):
			if not self.has_same_axis_as(other):
				raise ValueError("Axes are not aligned for the operation.")
		return np.add(self, other) 
	
	def __radd__(self, other):
		if isinstance(other, type(self)):
			if not self.has_same_axis_as(other):
				raise ValueError("Axes are not aligned for the operation.")
		return np.add(other, self)
	
	def __sub__(self, other):
		if isinstance(other, type(self)):
			if not self.has_same_axis_as(other):
				raise ValueError("Axes are not aligned for the operation.")
		return np.subtract(self, other)
	
	def __rsub__(self, other):
		if isinstance(other, type(self)):
			if not self.has_same_axis_as(other):
				raise ValueError("Axes are not aligned for the operation.")
		return np.subtract(other, self)
	
	def __mul__(self, other):
		if isinstance(other, type(self)):
			if not self.has_same_axis_as(other):
				raise ValueError("Axes are not aligned for the operation.")
		return np.multiply(self, other) 
	
	def __rmul__(self, other):
		if isinstance(other, type(self)):
			if not self.has_same_axis_as(other):
				raise ValueError("Axes are not aligned for the operation.")
		return np.multiply(other, self)
	
	def __truediv__(self, other):
		if isinstance(other, type(self)):
			if not self.has_same_axis_as(other):
				raise ValueError("Axes are not aligned for the operation.")
		return np.divide(self, other) 
	
	def __rtruediv__(self, other):
		if isinstance(other, type(self)):
			if not self.has_same_axis_as(other):
				raise ValueError("Axes are not aligned for the operation.")
		return np.divide(other, self)
	
	def __floordiv__(self, other):
		if isinstance(other, type(self)):
			if not self.has_same_axis_as(other):
				raise ValueError("Axes are not aligned for the operation.")
		return np.floor_divide(self, other) 
	
	def __rfloordiv__(self, other):
		if not self.has_same_axis_as(other):
			raise ValueError("Axes are not aligned for the operation.")
		return np.floor_divide(other, self)
	
	def __pow__(self, other):
		if isinstance(other, type(self)):
			if not self.has_same_axis_as(other):
				raise ValueError("Axes are not aligned for the operation.")
		return np.power(self, other) 
	
	def __rpow__(self, other):
		if isinstance(other, type(self)):
			if not self.has_same_axis_as(other):
				raise ValueError("Axes are not aligned for the operation.")
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
	
	
	#-----------------------------------
	# Utility Methods
	#-----------------------------------
	
	def unpack(self):
		"""
		Unpacks the object into easy to work
		with data structures.

		Returns
		-------
		(np.ndarray, np.ndarray, np.ndarray)
			- M: Signal data array.
			- y: Signal Y-axis array.
			- x: Signal X-axis array.
		"""
		
		M = self.M.values
		y = self.y.values
		x = self.x.values
		
		return (M, y, x)
	
	def copy(self) -> Self:
		"""
		Returns a new copy of the signal.

		Returns
		-------
		Self
			A new copy of the object.
		"""
		
		copied_M = self.M.copy()
		copied_y = self.y.copy()
		copied_x = self.x.copy()
		title = self.title # Immutable, hence no need to copy
		
		return self.__class__(M=copied_M, y=copied_y, x=copied_x, title=title)
	
	def set_meta_info(self, title = None, M_label = None, y_label = None, x_label = None) -> None:
		"""
		Set meta info about the signals.

		Parameters
		----------
		title: str
			- Title for the signal
			- e.g. "MyTitle"
		M_label: str
			- Label for the data that matrix is holding.
			- e.g. "Intensity (dB)"
		y_label: str
			- Label for the y-axis.
			- e.g. "Frequency (Hz)"
		x_label: str
			- Label for the x-axis.
			- e.g. "Time (sec)"
		Returns
		-------
		S2D
			A new instance with updated meta info.
		"""
		
		M, y, x = self.M, self.y, self.x
		
		M_label = str(M_label) if M_label is not None else M.label
		y_label = str(y_label) if y_label is not None else y.label
		x_label = str(x_label) if x_label is not None else x.label
		title = str(title) if title is not None else self.title
		
		# We create a new copy of the data and axis
		new_M = M.set_meta_info(label=M_label)
		new_y = y.set_meta_info(label=y_label)
		new_x = x.set_meta_info(label=x_label)
		
		return self.__class__(M=new_M, y=new_y, x=new_x, title=title)
	
	
	def is_same_as(self, other: Self) -> bool:
		"""
		Check if two `S1D` instances are equal.
		"""
		
		if not isinstance(other, type(self)):
			return False
		
		if not self.M.is_same_as(other.M):
			return False
		
		if not self.y.is_same_as(other.y):
			return False
		
		if not self.x.is_same_as(other.x):
			return False
		
		return True
	
	def has_same_axis_as(self, other) -> bool:
		"""
		Check if two 'S1D' instances have same
		axis. Many operations need to satify this.
		"""
		return self.y.is_same_as(other.y) and self.x.is_same_as(other.x)
	
	
	def mask(self, condition, set_to=None) -> Self:
		"""
		Mask the signal based on condition and
		the values can be set.
		
		Parameters
		----------
		condition: Callable
			- Condition function to apply on values of the signal.
			- E.g. lambda x: x > 10
		set_to: Number
			- Number to replace the masked position values.

		Returns
		-------
		S2D
			Masked Signal
		"""
		
		mask = condition(self)
		new_val = set_to
		
		if set_to is None: # Return the mask as the same signal but with booleans
			return mask
	
		else:
			# We apply the mask and update the signal data
			new_data = self.M.mask(condition=condition, set_to=new_val)
			
			# Since we're just updating the data, there is no change in the axis
			return self.__class__(M=new_data, y=self.y.copy(), x=self.x.copy(), title=self.title)
	
	#===================================
	
	
	
		
		
		
	#-----------------------------------
	# Visualisation
	#-----------------------------------
	
	def plot(
		self,
		ax = None,
		cmap = "gray_r",
		title = None,
		M_label = None,
		x_label = None,
		y_label = None,
		y_lim = None,
		x_lim = None,
		highlight_regions = None,
		vlines = None,
		hlines = None,
		origin = "lower",  # or "lower"
		gamma = None,
		show_colorbar = True,
		cax = None,
		show_grid = True,
		tick_mode = "center",  # "center" or "edge"
		n_ticks = None,
	) -> "plt.Figure":
		"""
		Plot the S2D instance using Matplotlib.
	
	
		Parameters
		----------
		ax : matplotlib.axes.Axes | None
			- If you want to plot the signal on a given matplotlib axes, you can pass the ax here. We do not return any figure in this case.
			- If not passed, we create a new figure, plots the signal on it and then return the figure.
		cmap : str, default "gray_r"
			Colormap used for the image.
		title : str | None
			- Title for the plot.
			- If not passed, we use the default set during signal instantiation.
		y_lim : tuple[float, float] | None
			- Limits for the y-axis.
		x_lim : tuple[float, float] | None
			- Limits for the x-axis.
		vlines: list[float]
			- List of x values to draw vertical lines.
			- e.g. [10, 13.5]
		hlines: list[float]
			- List of data values to draw horizontal lines.
			- e.g. [10, 13.5]
		highlight_regions : list[tuple[float, float, str]] | None
			- List of time intervals to highlight on the plot.
			- [(start, end, 'tag')]
		origin : {"lower", "upper"}, default "lower"
			Origin position for the image (for flipping vertical axis).
		gamma : float or int, optional
			If specified, apply log-compression using log(1 + S * factor).
		show_colorbar : bool
			- Whether to display the colorbar.
			- Defaults to True.
		cax : matplotlib.axes.Axes | None
			- Axis to draw the colorbar on. If None, uses default placement.
			- Defaults to None
		show_grid : bool
			- Whether to show the major gridlines.
			- Defaults to None.
		tick_mode : {"center", "edge"}
			- Whether to place ticks at bin centers or edges.
			- Default to "center"
		n_ticks : tuple[int]
			- Number of ticks (y_ticks, x_ticks) to display on each axis.
			- Defaults to None
	
		Returns
		-------
		matplotlib.figure.Figure | None
			- The figure object containing the plot.
			- None if ax is provided.
		"""
		from modusa.tools.plotter import Plotter
		
		M, y, x = self._M, self._y, self._x
		M_val, y_val, x_val = M._values, y._values, x._values
		
		M_label = M_label or M._label
		y_label = y_label or y._label
		x_label = x_label or x._label
		
		title = title or self._title
		
		fig = Plotter.plot_matrix(M=M_val, r=y_val, c=x_val, ax=ax, cmap=cmap, title=title, M_label=M_label, r_label=y_label, c_label=x_label, r_lim=y_lim, c_lim=x_lim,
		highlight_regions=highlight_regions, vlines=vlines, hlines=hlines, origin=origin, gamma=gamma, show_colorbar=show_colorbar, cax=cax, show_grid=show_grid,
		tick_mode=tick_mode, n_ticks=n_ticks)
		
		return fig
		
	#===================================
	
	#-----------------------------------
	# Information
	#-----------------------------------
	
	def print_info(self) -> None:
		"""Print key information about the signal."""
		
		print("-"*50)
		print(f"{'Title':<20}: {self._title}")
		print("-"*50)
		print(f"{'Type':<20}: {self.__class__.__name__}")
		print(f"{'Shape':<20}: {self.shape} (freq bins × time frames)")
		
		# Inheritance chain
		cls_chain = " → ".join(cls.__name__ for cls in reversed(self.__class__.__mro__[:-1]))
		print(f"{'Inheritance':<20}: {cls_chain}")
		print("=" * 50)
		
	def __str__(self):
		arr_str = np.array2string(
			np.asarray(self),
			separator=", ",
			threshold=20,       # limit number of elements shown
			edgeitems=2,          # show first/last 2 rows and columns
			max_line_width=120,   # avoid wrapping
		)
		return f"{self._nickname}({arr_str})"
	
	def __repr__(self):
		arr_str = np.array2string(
			np.asarray(self),
			separator=", ",
			threshold=20,       # limit number of elements shown
			edgeitems=2,          # show first/last 2 rows and columns
			max_line_width=120,   # avoid wrapping
		)
		return f"{self._nickname}({arr_str})"
	
	#===================================