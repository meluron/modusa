#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import immutable_property, validate_args_type
from .base import ModusaSignalData
from typing import Self, Any
import numpy as np

class Data(ModusaSignalData):
	"""
	Space to represent any modusa signal's data.

	Parameters
	----------
	values: array-like
		Data values as an array.
	label: str
		Label for the data.

	Note
	----
	- This is only for developers reference.
	- As a user of the library, you will never instantiate this class.
	- It is used internally and users will be provided APIs to interact with this class if necessary.	
	"""
	
	#--------Meta Information----------
	_name = "Data"
	_nickname = "data" # This is to be used in repr/str methods
	_description = "Space to represent any signal's data."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-27"
	#----------------------------------
	
	def __init__(self, values, label=None):
		super().__init__() # Instantiating `ModusaSignalData` class
		
		values = np.asarray(values)
		
		if values.ndim > 2:
			raise ValueError("We do not currently support, > 2 dim arrays, please create a GitHub issue")
		
		self._values = values
		self._label = label or ""
	
	#-----------------------------------
	# Properties
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
	def ndim(self) -> tuple:
		return self.values.ndim
	
	@property
	def size(self) -> int:
		return self.values.size
	
	#===================================

	#-------------------------------
	# Utility methods
	#-------------------------------
	
	def is_same_as(self, other) -> bool:
		"""
		Check if two data instances are same.

		Parameters
		----------
		other: Data
			Another Data object to compare with.
		
		Returns
		-------
		bool
			True if same ow False

		Note
		----
		- We check the shape and all the values.
		- We are not checking the labels for now.
		"""
		
		arr1 = np.asarray(self)
		arr2 = np.asarray(other)
		
		if isinstance(other, type(self)):
			return False
		if arr1.shape != arr2.shape:
			return False
		if not np.allclose(arr1, arr2):
			return False
		
		return True
	
	def copy(self) -> Self:
		"""
		Return a new copy of data object.
		
		Returns
		-------
		Data
			A new copy of the data object.
		"""
		copied_values = np.asarray(self).copy()
		copied_label = self.label
		
		return self.__class__(values=copied_values, label=copied_label)
	
	def set_meta_info(self, label):
		"""
		Set meta info for the data.
		
		Parameters
		----------
		label: str
			Label for the data (e.g. "Intensity (dB)").
		Returns
		-------
		Self
			A new Self instance with new label.
		"""
		
		if label is None:
			return self
		else:
			return self.__class__(values=self.values.copy(), label=label)
		
	def mask(self, condition, set_to=None) -> Self:
		"""
		Mask the data based on condition and
		the values can be set using the `set_to` argument.
		
		Parameters
		----------
		condition: Callable
			- Condition function to apply on values of the data.
			- E.g. lambda x: x > 10
		set_to: Number
			- Number to replace the masked position values.

		Returns
		-------
		Data
			Masked Data with either booleans as per the condition or with updated values.
		"""
		
		mask = condition(self)
		new_value = set_to
		
		if new_value is None: # Return the mask as the same signal but with booleans
			return mask
	
		else:
			# We apply the mask and update the signal data
			data_arr = self.values.copy() # We do not want to modify the data inplace
			data_arr[mask] = new_value
			
			updated_data = Data(values=data_arr, label=self.label)
			
			return updated_data
	
	def pad(self, left=None, right=None) -> Self:
		"""
		Pad the data from left or right.

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
		
		values = np.asarray(self).copy()
		if self.ndim == 1: # 1D
			if isinstance(left, (int, float)): left = [left]
			if isinstance(right, (int, float)): right = [right]
			
			if left is not None:
				values = np.concatenate((left, values))
			if right is not None:
				values = np.concatenate((values, right))
				
			return self.__class__(values=values, label=self.label)
			
		elif self.ndim == 2: # 2D
			if isinstance(left, (int, float)): left = [left]
			if isinstance(right, (int, float)): right = [right]
			
			if left is not None:
				left = np.asarray(left)
				if left.ndim != 1:
					raise ValueError(f"left must be 1 dimension")
				left_cols = np.tile(left, (self.shape[0], 1))
				values = np.concatenate((left_cols, values), axis=1)
				
			if right is not None:
				right = np.asarray(right)
				if right.ndim != 1:
					raise ValueError(f"right must be 1 dimension")
				right_cols = np.tile(right, (self.shape[0], 1))
				values = np.concatenate((values, right_cols), axis=1)
			
			return self.__class__(values=values, label=self.label)
			
	
	#================================
	
	
	#-------------------------------
	# NumPy Protocol
	#-------------------------------
	def __array__(self, dtype=None) -> np.ndarray:
		return np.asarray(self.values, dtype=dtype)
	
	def __index__(self):
		return int(self.values)
	
	def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
		"""
		Provides operation support for the universal functions
		on the Data object.

		"""
		
		raw_inputs = [x.values if isinstance(x, type(self)) else x for x in inputs]
		
		# Call the actual ufunc
		result = getattr(ufunc, method)(*raw_inputs, **kwargs)
		
		if isinstance(result, (np.ndarray, np.generic)):
			return self.__class__(result, label=self.label)
		else:
			return result
	
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
		data = args[0]
		data_arr = np.asarray(data)
		if "keepdims" not in kwargs: # We keep keepdim to True by default so that we remain in the same signal space.
			kwargs["keepdims"] = True
		result_arr = func(data_arr, **kwargs)
		
		if func in nfc.REDUCTION_FUNCS:
			return self.__class__(values=result_arr, label=data.label)
		
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
		key : int | slice | tuple
			Index to apply to the values.
	
		Returns
		-------
		Data
			A new Data object with sliced values and same metadata,
			with singleton dimensions restored to match axis alignment.
		"""
		if not isinstance(key, (int, slice, tuple)):
			raise TypeError(f"Invalid key type {type(key)}")
			
		if self.ndim > 2:
			raise ValueError("Support for upto 2 dim only")
			
		sliced_arr = self.values[key]
		
		# Case 1: 1D array
		if self.ndim == 1:
			if sliced_arr.ndim == 0: # We have 
				# We need to make it 1D
				sliced_arr = np.expand_dims(sliced_arr, axis=0)
			
		# Case 2: 2D array
		if self.ndim == 2:
			if sliced_arr.ndim == 0:
				# We need to make it 2D
				sliced_arr = np.expand_dims(sliced_arr, axis=0)
				sliced_arr = np.expand_dims(sliced_arr, axis=0)
			elif sliced_arr.ndim == 1:
				if isinstance(key, int):
					axis_of_interest = 0
				# Assumption is that key is tuple of len 2 with atleast one position being integer, that is our axis of interest
				elif isinstance(key, tuple) and len(key) == 2:
					if isinstance(key[0], int):
						axis_of_interest = 0
					elif isinstance(key[1], int):
						axis_of_interest = 1
				# We need to make it 2D but based on the axis
				sliced_arr = np.expand_dims(sliced_arr, axis=axis_of_interest)
		
		return self.__class__(values=sliced_arr, label=self.label)
	
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
		if not isinstance(key, (int, slice, tuple)):
			raise TypeError(f"Invalid key type {type(key)}")
			
		self.values[key] = value  # In-place assignment
	
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
	
	#-------------------------------
	# Representation
	#-------------------------------
	
	def __str__(self):

		arr_str = np.array2string(
			np.asarray(self),
			separator=", ",
			threshold=30,       # limit number of elements shown
			edgeitems=3,          # show first/last 3 rows and columns
			max_line_width=120,   # avoid wrapping
		)
		
		return f"{self._nickname}({arr_str})"
	
	def __repr__(self):
		
		arr_str = np.array2string(
			np.asarray(self),
			separator=", ",
			threshold=30,       # limit number of elements shown
			edgeitems=3,          # show first/last 3 rows and columns
			max_line_width=120,   # avoid wrapping
		)
		
		return f"{self._nickname}({arr_str})"
	
	#===============================