#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import immutable_property, validate_args_type
from .s2d import S2D
from .s_ax import SAx
from .t_ax import TAx
from .data import Data
from modusa.tools.math_ops import MathOps
from typing import Self, Any, Callable
import numpy as np
import matplotlib.pyplot as plt
import modusa as ms

class FTDS(S2D):
	"""
	Space to represent feature time domain signal (2D).

	Note
	----
	- Use :class:`~modusa.generators.ftds.FTDSGen` API to instantiate this class.
	- The signal must have uniform time axis thus `TAx`.

	Parameters
	----------
	M: Data
		- Data object holding the main 2D array.
	f: SAx
		- Feature-axis of the 2D signal.
	t: TAx
		- Time-axis of the 2D signal.
	title: str
		- What does the signal represent?
		- e.g. "MySignal"
		- This is used as the title while plotting.
	"""
	
	#--------Meta Information----------
	_name = "Feature Time Domain Signal"
	_nickname = "FTDS" # This is to be used in repr/str methods
	_description = "Space to represent feature time domain signal (2D)."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-21"
	#----------------------------------
	
	def __init__(self, M, f, t, title = None):
		
		if not (isinstance(M, Data) and isinstance(f, SAx), isinstance(t, TAx)):
			raise TypeError(f"`M` must be `Data` instance, `f` and `x` must be `SAx` and `TAx` instances, got {type(M)}, {type(f)} and {type(t)}")
		
		super().__init__(M=M, y=f, x=t, title=title) # Instantiating `ModusaSignal` class
	
	#--------------------------------------
	# Properties
	#--------------------------------------
		
	@property
	def M(self) -> Data:
		return self._M
	
	@property
	def f(self) -> SAx:
		return self._y
	
	@property
	def t(self) -> SAx:
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
	
	#===================================
	
		
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
		f = self.f.copy()
		t = self.t.copy()
		
		if result.shape[0] != f.shape[0] or result.shape[1] != t.shape[0]:
			raise ValueError(f"`{ufunc.__name__}` caused shape mismatch between data and axis, please create a github issue")
			
		return self.__class__(M=result, f=f, t=t, title=self.title)
	
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
					dummy_f = SAx(0, "")
					dummy_t = TAx(n_points=1, sr=signal.t.sr, t0=0.0, label="")
					return self.__class__(M=result, f=dummy_f, t=dummy_t, title=signal.title)
			
				if isinstance(axis, int): # One of the axis collapsed
					if axis == 0:
						dummy_f = SAx(0, "")
						return self.__class__(M=result, f=dummy_f, t=signal.t.copy(), title=signal.title)
					elif axis in [1, -1]:
						dummy_t = TAx(n_points=1, sr=signal.t.sr, t0=0.0, label="")
						return self.__class__(M=result, f=signal.f.copy(), t=dummy_t, title=signal.title)
					else:
						raise ValueError
			elif keepdims is False:
				if axis is None: # Return Data
					return result
				if axis == 0: # Return TDS
					from .tds import TDS
					return TDS(y=result, t=signal.t, title=signal.title)
				elif axis in [1, -1]: # Return S1D
					from .s1d import S1D
					return S1D(y=result, x=signal.f, title=signal.title)
				else:
					raise ValueError
							
	
			# Case 3: Reduction keeps both axes (unlikely)
			else:
				raise NotImplementedError(f"{func.__name__} result shape={result.shape} not handled for modusa signal")
				
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
		S2D | S1D | Data
			- S2D object if slicing results in 2D array
			- S1D object if slicing results in 1D array
			- Data if slicing results in scalar
		"""
		from .s1d import S1D
		from .tds import TDS
		
		if isinstance(key, S1D):
			raise TypeError(f"Applying `S1D` mask on `S2D` is not allowed.")
			
		# We slice the data
		sliced_M = self.M[key]
		
		# Case 1: Row indexing only — return a horizontal slice (1D view across columns)
		if isinstance(key, int):
			sliced_f = self.f[key]
			sliced_t = self.t
			return TDS(y=sliced_M, x=sliced_t, title=self.title)
		
		# Case 2: Column indexing only — return a vertical slice (1D view across rows)
		elif isinstance(key, slice):
			sliced_f = self.f[key]
			sliced_t = self.t
			return self.__class__(M=sliced_M, f=sliced_f, t=sliced_t, title=self.title)
		
		# Case 3: 2D slicing
		elif isinstance(key, tuple) and len(key) == 2:
			row_key, col_key = key
			if isinstance(row_key, int) and isinstance(col_key, int):
				# Single value extraction → shape = (1, 1)
				# Will return data object
				return Data(values=sliced_M, title=self.title)
			
			elif isinstance(row_key, int) and isinstance(col_key, slice):
				# Row vector → return S1D
				sliced_f = self.f[row_key] # Scalar
				sliced_t = self.t[col_key]
				
				return TDS(y=sliced_M, t=sliced_t, title=self.title)
			
			elif isinstance(row_key, slice) and isinstance(col_key, int):
				# Column vector → return S1D
				sliced_f = self.f[row_key]
				sliced_t = self.t[col_key] # Scalar
				
				return S1D(y=sliced_M, x=sliced_f, title=self.title)
			
			elif isinstance(row_key, slice) and isinstance(col_key, slice):
				# 2D slice → return same class
				sliced_f = self.f[row_key]
				sliced_t = self.t[col_key] 
				
				return self.__class__(M=sliced_M, f=sliced_f, t=sliced_t, title=self.title)
		
		# Case 4: Boolean masking signal
		elif isinstance(key, type(self)):
			sliced_f = self.f
			sliced_t = self.t
			
			return self.__class__(M=sliced_M, f=sliced_f, t=sliced_t, title=self.title)
		
		else:
			raise TypeError(f"Unsupported index type: {type(key)}")
			
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
	
	#====================================
	
	
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
			- f: Signal feature-axis array.
			- t: Signal time-axis array.
		"""
		
		M = self.M.values
		f = self.f.values
		t = self.t.values
		
		return (M, f, t)
	
	def copy(self) -> Self:
		"""
		Returns a new copy of the signal.

		Returns
		-------
		Self
			A new copy of the object.
		"""
		
		copied_M = self.M.copy()
		copied_f = self.f.copy()
		copied_t = self.t.copy()
		title = self.title # Immutable, hence no need to copy
		
		return self.__class__(M=copied_M, f=copied_f, t=copied_t, title=title)
	
	def set_meta_info(self, title = None, M_label = None, f_label = None, t_label = None) -> None:
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
		f_label: str
			- Label for the feature-axis.
			- e.g. "Frequency (Hz)"
		t_label: str
			- Label for the time-axis.
			- e.g. "Time (sec)"
		Returns
		-------
		FTDS
			A new instance with updated meta info.
		"""
		
		M, f, t = self.M, self.f, self.t
		
		M_label = str(M_label) if M_label is not None else M.label
		f_label = str(f_label) if f_label is not None else f.label
		t_label = str(t_label) if t_label is not None else t.label
		title = str(title) if title is not None else self.title
		
		# We create a new copy of the data and axis
		new_M = M.set_meta_info(label=M_label)
		new_f = f.set_meta_info(label=f_label)
		new_t = t.set_meta_info(label=t_label)
		
		return self.__class__(M=new_M, f=new_f, t=new_t, title=title)
	
	def translate_t(self, n_samples):
		"""
		Translate the FTDS signal along time axis
		by `n_samples`.

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
		FTDS
			Translated signal.
		"""
		
		# We just need to create a new time axis with shifted t0
		translated_t = self.t.translate(n_samples=n_samples)
		
		translated_signal = self.__class__(M=self.M.copy(), f=self.f.copy(), t=translated_t, title=self.title)
		
		return translated_signal
	
	
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
			return self.__class__(M=new_data, f=self.f.copy(), t=self.t.copy(), title=self.title)
		
		
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
		FTDS
			Padded signal.
		"""
		
		if right is None and left is None: # No padding applied
			return self
	
		# Pad the data
		M_padded = self.M.pad(left=left, right=right)
	
		# Find the new t0
		if left is not None:
			if np.ndim(left) == 0: left = np.asarray([left])
			else: left = np.asarray(left)
			new_t0 = self.t.t0 - (left.shape[0] / self.t.sr)
		else:
			new_t0 = self.t.t0

		t_padded = self.t.__class__(n_points=M_padded.shape[1], sr=self.t.sr, t0=new_t0, label=self.t.label)
		
		return self.__class__(M=M_padded, f=self.f.copy(), t=t_padded, title=self.title)
	
	#====================================
	
	
	
	
	#-----------------------------------
	# Info
	#-----------------------------------
	
	def print_info(self) -> None:
		"""Print key information about the FTDS signal."""
		print("-"*50)
		print(f"{'Title':<20}: {self.title}")
		print("-"*50)
		print(f"{'Type':<20}: {self.__class__.__name__}")
		print(f"{'Shape':<20}: {self.shape} (freq bins × time frames)")
		print(f"{'Duration':<20}: {self.t.duration}")
		print(f"{'Frame Rate':<20}: {self.t.sr} (frames / sec)")
		print(f"{'Frame Duration':<20}: {1 / self.t.sr:.4f} sec ({(1 / self.t.sr) * 1000:.2f} ms)")
		
		# Inheritance chain
		cls_chain = " → ".join(cls.__name__ for cls in reversed(self.__class__.__mro__[:-1]))
		print(f"{'Inheritance':<20}: {cls_chain}")
		print("=" * 50)
		
		
	#===================================