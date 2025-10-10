#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import immutable_property, validate_args_type
from .base import ModusaSignal
from .data import Data
from .s_ax import SAx
from .t_ax import TAx
from modusa.tools.math_ops import MathOps
from typing import Self, Any, Callable
from types import NoneType
import numpy as np
import matplotlib.pyplot as plt
import copy

class S1D(ModusaSignal):
	"""
	Space to represent any 1D Signal.
	
	Note
	----
	- Use :class:`~modusa.generators.s1d.S1DGen` API to instantiate this class.
	- The signal can have uniform/non-uniform axis.


	Parameters
	----------
	data: Data
		- Data object holding the main array.
	sax: SAx
		- Axis for the signal.
	title: str
		- Title for the signal.
		- Default: None => ''
		- This is used as the title while plotting.
	"""
	
	#--------Meta Information----------
	_name = "Signal 1D"
	_nickname = "signal" # This is to be used in repr/str methods
	_description = "Space to represent any 1D Signal."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-20"
	#----------------------------------
	
	def __init__(self, y, x, title = None):
		super().__init__() # Instantiating `ModusaSignal` class
		
		if not (isinstance(y, Data) and isinstance(x, SAx)):
			raise TypeError(f"`y` must be `Data` instance and `x` must be `SAx` instance, got {type(y)} and {type(x)}")
		
		assert y.ndim == 1
		assert y.shape == x.shape, f"y and x shape must match"
		
		# All these are private and we do not expose it to users directly.
		self._y = y
		self._x = x
		self._title = title or self._name
		
	
	#-----------------------------------
	# Properties (User Facing)
	#-----------------------------------
	
	@property
	def y(self) -> Data:
		return self._y
	
	@property
	def x(self) -> SAx:
		return self._x
	
	@property
	def title(self) -> str:
		return self._title
	
	@property
	def shape(self) -> tuple:
		return self.y.shape
	
	@property
	def ndim(self) -> int:
		return self.y.ndim # Should be 1
	
	@property
	def size(self) -> int:
		return self.y.size
	
	#===================================
	
	#-------------------------------
	# NumPy Protocol
	#-------------------------------
	
	def __array__(self, dtype=None) -> np.ndarray:
		return np.asarray(self.y.values, dtype=dtype)
	
	def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
		"""
		Supports NumPy universal functions on the Signal1D object.
		"""
		from .data import Data  # Ensure this is the same Data class you're using
		from modusa.utils import np_func_cat as nfc
		
		raw_inputs = [
			np.asarray(obj.y) if isinstance(obj, type(self)) else obj
			for obj in inputs
		]
		
		result = getattr(ufunc, method)(*raw_inputs, **kwargs)
		
		y = Data(values=result, label=None)  # label=None or you could copy from self.y.label
		x = self.x.copy()
		
		if y.shape != x.shape:
			raise ValueError(f"`{ufunc.__name__}` caused shape mismatch between data and axis, please create a github issue")
		
		return self.__class__(y=y, x=x, title=self.title)
		
	def __array_function__(self, func, types, args, kwargs):
		"""
		Additional numpy function support.
		"""
		from modusa.utils import np_func_cat as nfc
		
		if not all(issubclass(t, type(self)) for t in types):
			return NotImplemented
		
		# Not supporting concatenate like operations as axis any random axis can't be concatenated
		if func in nfc.CONCAT_FUNCS:
			raise NotImplementedError(f"`{func.__name__}` is not yet tested on modusa signal, please create a GitHub issue.")

		# Single signal input expected
		signal = args[0]
		result: Data = func(signal.y, **kwargs)
		axis = kwargs.get("axis", None)
		keepdims = kwargs.get("keepdims", None)
	
		if func in nfc.REDUCTION_FUNCS:
			if keepdims is None or keepdims is True: # Default state is True => return 1D signal by wrapping the scalar
				from .s_ax import SAx
				dummy_x = SAx(0, "")
				return self.__class__(y=result, x=dummy_x, title=signal.title)
			elif keepdims is False: # Return Data
				from .data import Data
				return Data(values=result, label=None)
	
		elif func in nfc.X_NEEDS_ADJUSTMENT_FUNCS:
			# You must define logic for adjusting x
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
		key : int | slice | S1D
			- Index to apply to the values.
		
		Returns
		-------
		S1D
			A new S1D object with sliced values and same meta data.
		"""
		
		if not isinstance(key, (int, slice)):
			raise TypeError(f"Invalid key type: {type(key)}")
		
		sliced_y = self.y[key]
		sliced_x = self.x[key]
		
		return self.__class__(y=sliced_y, x=sliced_x, title=self.title)
	
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
		
		if not isinstance(key, (int, slice)):
			raise TypeError(f"Invalid key type: {type(key)}")
		
		self.y[key] = value  # In-place assignment
		
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
		(np.ndarray, np.ndarray)
			- y: Signal data array.
			- x: Signal axis array.
		"""
		
		y = self.y.values
		x = self.x.values
		
		return (y, x)
	
	def copy(self) -> Self:
		"""
		Returns a new copy of the signal.

		Returns
		-------
		Self
			A new copy of the object.
		"""
		copied_y = self.y.copy()
		copied_x = self.x.copy()
		title = self.title # Immutable, hence no need to copy
		
		return self.__class__(y=copied_y, x=copied_x, title=title)
	
	def set_meta_info(self, title=None, y_label=None, x_label=None) -> None:
		"""
		Set meta info about the signal.

		Parameters
		----------
		title: str
			- Title for the signal
			- e.g. "Speedometer"
		y_label: str
			- Label for the y-axis.
			- e.g. "Speeed (m/s)"
		x_label: str
			- Label for the x-axis.
			- e.g. "Distance (m)"
		"""
		
		y, x = self.y, self.x
		
		new_title = str(title) if title is not None else self.title
		new_y_label = str(y_label) if y_label is not None else y.label
		new_x_label = str(x_label) if x_label is not None else x.label
		
		# We create a new copy of the data and axis
		new_y = y.__class__(values=y.values().copy(), label=y_label)
		new_x = x.__class__(values=x.values().copy(), label=x_label)
		
		return self.__class__(y=new_y, x=new_x, title=title)
	
	
	def is_same_as(self, other: Self) -> bool:
		"""
		Check if two `S1D` instances are equal.
		"""
		
		if not isinstance(other, type(self)):
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
		return self.x.is_same_as(other.x)
	
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
		S1D
			Masked Signal
		"""
		
		mask = condition(self)
		new_val = set_to
		
		if set_to is None: # Return the mask as the same signal but with booleans
			return mask
		
		else:
			# We apply the mask and update the signal data
			new_data = self.y.mask(condition=condition, set_to=new_val)
			
			# Since we're just updating the data, there is no change in the axis
			return self.__class__(y=new_data, x=self.x.copy(), title=self.title)
	
	#===================================
	
	#-----------------------------------
	# Tools
	#-----------------------------------
	
	def plot(
		self,
		ax = None,
		fmt: str = "k-",
		title = None,
		y_label = None,
		x_label = None,
		y_lim = None,
		x_lim = None,
		highlight_regions = None,
		vlines = None,
		hlines = None,
		legend = None,
		show_grid = True,
		show_stem = False,
	) -> plt.Figure | None:
		"""
		Plot the signal.
		
		.. code-block:: python
		
			import modusa as ms
			import numpy as np
			signal = ms.S1D(data=np.random.random(100), data_label="My data (unit)", title="My Random Signal")
			display(signal.plot())
		
		Parameters
		----------
		ax : matplotlib.axes.Axes | None
			- If you want to plot the signal on a given matplotlib axes, you can pass the ax here. We do not return any figure in this case.
			- If not passed, we create a new figure, plots the signal on it and then return the figure.
		fmt : str
			- Format of the plot as per matplotlib standards (Eg. "k-" or "blue--o)
			- Default is "k-"
		title : str | None
			- Title for the plot.
			- If not passed, we use the default set during signal instantiation.
		y_label : str | None
			- Label for the y-axis.
			- If not passed, we use the default set during signal instantiation.
		x_label : str | None
			- Label for the x-axis.
			- If not passed, we use the default set during signal instantiation.
		y_lim : tuple[float, float] | None
			- Limits for the y-axis.
		x_lim : tuple[float, float] | None
			- Limits for the x-axis.
		highlight_regions : list[tuple[float, float, str]] | None
			- List of time intervals to highlight on the plot.
			- [(start, end, 'tag')]
		vlines: list[float]
			- List of x values to draw vertical lines.
			- e.g. [10, 13.5]
		hlines: list[float]
			- List of data values to draw horizontal lines.
			- e.g. [10, 13.5]
		show_grid: bool
			- If true, shows grid.
			- Default: True
		show_stem : bool
			- If True, use a stem plot instead of a continuous line. 
			- Autorejects if signal is too large.
		legend : str | tuple[str, str] | None
			- If provided, adds a legend at the specified location.
			- e.g., "signal" -> gets converted into ("signal", "best")
			- e.g. ("signal", "upper right")
		
		Returns
		-------
		matplotlib.figure.Figure | None
			- The figure object containing the plot.
			- None in case an axis is provided.

		See Also
		--------
		modusa.tools.plotter.Plotter
		"""
		
		from modusa.tools.plotter import Plotter
		
		y: Data = self._y
		x: SAx = self._x
		y_val = y._values
		x_val = x._values
		
		if y_label is None: y_label = self._y._label
		if x_label is None: x_label = self._x._label
		if title is None: title = self.title
		
		fig: plt.Figure | None = Plotter.plot_signal(y=y_val, x=x_val, ax=ax, fmt=fmt, title=title, y_label=y_label, x_label=x_label, y_lim=y_lim, x_lim=x_lim, highlight_regions=highlight_regions, vlines=vlines, hlines=hlines, show_grid=show_grid, show_stem=show_stem, legend=legend)
		
		return fig
	
	#===================================
	
	
	
	#----------------------------------
	# Information
	#----------------------------------
	
	def print_info(self) -> None:
		"""Prints info about the audio."""
		print("-" * 50)
		print(f"{'Title'}: {self._title}")
		print("-" * 50)
		print(f"{'Type':<20}: {self.__class__.__name__}")
		print(f"{'Shape':<20}: {self.shape}")
		
		# Inheritance chain
		cls_chain = " → ".join(cls.__name__ for cls in reversed(self.__class__.__mro__[:-1]))
		print(f"{'Inheritance':<20}: {cls_chain}")
		print("=" * 50)
	
	def __str__(self):
		y, x = self._y, self._x
		y_label = y._label
		y_val = y._values
		shape = self.shape
		
		
		arr_str = np.array2string(
			y_val,
			separator=", ",
			threshold=30,       # limit number of elements shown
			edgeitems=2,          # show first/last 3 rows and columns
			max_line_width=120,   # avoid wrapping
		)
		
		return f"{self._nickname}({arr_str})"
		
	def __repr__(self):
		y, x = self._y, self._x
		y_label = y._label
		y_val = y._values
		shape = self.shape
		
		arr_str = np.array2string(
			y_val,
			separator=", ",
			threshold=30,       # limit number of elements shown
			edgeitems=2,          # show first/last 3 rows and columns
			max_line_width=120,   # avoid wrapping
		)
		return f"{self._nickname}({arr_str})"
	#===================================