#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import immutable_property, validate_args_type
from .s1d import S1D
from .t_ax import TAx
from .data import Data
from modusa.tools.math_ops import MathOps
from typing import Self, Any, Callable
from types import NoneType
import numpy as np
import matplotlib.pyplot as plt

class TDS(S1D):
	"""
	Space to represent time domain signals.
	
	Note
	----
	- Use :class:`~modusa.generators.tds.TDSGen` to instantiate this class.

	Parameters
	----------
	y: Data
		- Data object holding the main array.
	t: TAx
		- Time axis for the signal.
	title: str
		- Title for the signal.
		- Default: None => ''
		- e.g. "MySignal"
		- This is used as the title while plotting.
	"""
	
	#--------Meta Information----------
	_name = "Time Domain Signal"
	_nickname = "signal" # This is to be used in repr/str methods
	_description = "Space to represent uniform time domain signal."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-20"
	#----------------------------------
	

	def __init__(self, y, t, title = None):
		
		if not (isinstance(y, Data) and isinstance(t, TAx)):
			raise TypeError(f"`y` must be `Data` instance and `t` must be `TAx` object, got {type(y)} and {type(x)}")
			
		assert y.ndim == 1
		
		super().__init__(y=y, x=t, title=title) # Instantiating `Signal1D` class
	
	#---------------------------------
	# Properties (Hidden)
	#---------------------------------
	
	@property
	def y(self) -> Data:
		return self._y
	
	@property
	def t(self) -> TAx:
		return self.x
	
	@property
	def title(self) -> str:
		return self._title
	
	@property
	def shape(self) -> tuple:
		return self.y.shape
	
	@property
	def ndim(self) -> tuple:
		return self.y.ndim # Should be 1
	
	@property
	def size(self) -> int:
		return self.y.size
	
	#==================================
	
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
		t = self.t.copy()
		
		if y.shape != t.shape:
			raise ValueError(f"`{ufunc.__name__}` caused shape mismatch between data and axis, please create a github issue")
			
		return self.__class__(y=y, t=t, title=self.title)
	
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
				from .t_ax import TAx
				dummy_t = TAx(n_points=1, sr=signal.t.sr, t0=0, label=None)
				return self.__class__(y=result, t=dummy_t, title=signal.title)
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
		key : array-like
			- Index to apply to the values.
		
		Returns
		-------
		TDS
			A new TDS object with sliced values and same meta data.
		"""
		if not isinstance(key, (int, slice)):
			raise TypeError(f"Invalid key type: {type(key)}")
		
		sliced_y = self.y[key]
		sliced_t = self.t[key]
		
		if sliced_y.ndim == 0:
			sliced_y = Data(values=sliced_y.values, label=sliced_y.label, ndim=1)
			
		return self.__class__(y=sliced_y, t=sliced_t, title=self.title)
	
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
		
		self.y[key] = value  # In-place assignment
		
	#===================================
	
	
	#-----------------------------------
	# Utility Methods
	#-----------------------------------
	
	def unpack(self):
		"""
		Unpacks the object into easy to work
		with data structures.

		Returns
		-------
		(np.ndarray, float, float)
			- y: Signal data array.
			- sr: Sampling rate of the signal.
			- t0: Starting timestamp.
		"""
		
		arr = self.y.values
		sr = self.t.sr
		t0 = self.t.t0
		
		return (arr, sr, t0)
		
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
		
	
	def set_meta_info(self, title = None, y_label = None, t_label = None) -> None:
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
		t_label: str
			- Label for the time-axis.
			- e.g. "Distance (m)"
		"""
		
		new_title = str(title) if title is not None else self.title
		new_y_label = str(y_label) if y_label is not None else self.y.label
		new_t_label = str(t_label) if t_label is not None else self.t.label
		
		# We create a new copy of the data and axis
		new_y = self.y.copy().set_meta_info(y_label)
		new_t = self.t.copy().set_meta_info(t_label)
		
		return self.__class__(y=new_y, t=new_t, title=title)
	
	
	def is_same_as(self, other: Self) -> bool:
		"""
		Check if two `TDS` instances are equal.
		"""
		
		if not isinstance(other, type(self)):
			return False
		
		if not self.y.is_same_as(other.y):
			return False
		
		if not self.t.is_same_as(other.t):
			return False
		
		return True
	
	def has_same_axis_as(self, other) -> bool:
		"""
		Check if two 'TDS' instances have same
		axis. Many operations need to satify this.
		"""
		return self.t.is_same_as(other.t)
	
	
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
		TDS
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
			return self.__class__(y=new_data, t=self.t.copy(), title=self.title)
	#===================================
	
	#-------------------------------
	# Tools
	#-------------------------------
		
	@validate_args_type()
	def translate_t(self, n_samples: int):
		"""
		Translate the signal along time axis.
		
		Note
		----
		- Negative indexing is allowed but just note that you might end up getting time < 0


		.. code-block:: python
			
			import modusa as ms
			s1 = ms.tds([1, 2, 4, 4, 5, 3, 2, 1])
			ms.plot(s1, s1.translate_t(-1), s1.translate_t(3))
		
		Parameters
		----------
		n_samples: int
			By how many sample you would like to translate the signal.
		
		Returns
		-------
		TDS
			Translated signal.
		"""
		
		translated_t = self.t.translate(n_samples=n_samples)
		
		return self.__class__(y=self.y.copy(), t=translated_t, title=self.title)
	
	def pad(self, left=None, right=None) -> Self:
		"""
		Pad the signal with array like object from the
		left or right.

		Parameters
		----------
		left: arraylike
			- What to pad to the left of the signal.
			- E.g. 1 or [1, 0, 1], np.array([1, 2, 3])
		right: arraylike
			- What to pad to the right of the signal.
			- E.g. 1 or [1, 0, 1], np.array([1, 2, 3])

		Returns
		-------
		TDS
			Padded signal.
		"""
		
		if right is None and left is None: # No padding applied
			return self
		
		# Pad the data
		y_padded = self.y.pad(left=left, right=right)
			
		# Find the new t0
		if left is not None:
			if np.ndim(left) == 0: left = np.asarray([left])
			else: left = np.asarray(left)
			new_t0 = self.t.t0 - (left.shape[0] / self.t.sr)
		else:
			new_t0 = self.t.t0
		
		t_padded = self.t.__class__(n_points=y_padded.shape[0], sr=self.t.sr, t0=new_t0, label=self.t.label)
		
		return self.__class__(y=y_padded, t=t_padded, title=self.title)
		
		
	
	def crop(self, t_min = None, t_max = None, like = None) -> Self:
		"""
		Crop the signal to a time range [t_min, t_max].

		.. code-block:: python

			import modusa as ms
			s1 = ms.tds.random(1000, sr=10)
			ms.plot(s1, s1.crop(5, 40), s1.crop(20), s1.crop(60, 80))

	
		Parameters
		----------
		t_min : float or None
			Inclusive lower time bound in second (other units). If None, no lower bound.
		t_max : float or None
			Exclusive upper time bound in second (other units). If None, no upper bound.
		like: TDS
			- A `TDS` object whose start and end time will be used.
			- If you have a window signal, you can crop the signal to get the correct portion.
		
		Returns
		-------
		TDS
			Cropped signal.
		"""
		
		if like is not None:
			ref_signal = like
			assert self.t.sr == ref_signal.t.sr
			# Set t_min and t_max as per the signal
			t_min = ref_signal.t.t0
			t_max = ref_signal.t.end_time
		
		# We first will find out the time in samples
		if t_min is not None:
			t_min_sample = self.t.index_of(t_min)
		else:
			t_min_sample = 0
			
		if t_max is not None:
			t_max_sample = self.t.index_of(t_max)
		else:
			t_max_sample = -1
		
		return self[t_min_sample: t_max_sample+1]
	
	#===================================
	
	#-----------------------------------
	# Information
	#-----------------------------------
	
	def print_info(self) -> None:
		"""Prints info about the audio."""
		print("-" * 50)
		print(f"{'Title'}: {self.title}")
		print("-" * 50)
		print(f"{'Type':<20}: {self.__class__.__name__}")
		print(f"{'Shape':<20}: {self.shape}")
		print(f"{'Duration':<20}: {self.t.duration:.2f} sec")
		print(f"{'Sampling Rate':<20}: {self.t.sr} Hz")
		print(f"{'Sampling Period':<20}: {(1 / self.t.sr * 1000):.2f} ms")
		
		# Inheritance chain
		cls_chain = " → ".join(cls.__name__ for cls in reversed(self.__class__.__mro__[:-1]))
		print(f"{'Inheritance':<20}: {cls_chain}")
		print("=" * 50)
	
	#======================================