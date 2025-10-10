#!/usr/bin/env python3

from modusa import excp
from modusa.tools.base import ModusaTool
from typing import Any
import numpy as np

class MathOps(ModusaTool):
	"""
	Performs arithmetic and NumPy-style ops.

	Note
	----
	- Shape-changing operations like reshape, transpose, etc. are not yet supported. Use only element-wise or aggregation ops for now. 
	- Index alignment must be handled carefully in future extensions.
	"""
	
	def _axes_match(a1: tuple[np.ndarray, ...], a2: tuple[np.ndarray, ...]) -> bool:
		"""
		To check if two axes are same.

		It checks the length of the axes and the corresponding values.
		"""
		if len(a1) != len(a2):
			return False
		return all(np.allclose(x, y, atol=1e-8) for x, y in zip(a1, a2))
	
	
	#----------------------------------
	# To handle basic element wise 
	# math operations like
	# +, -, *, **, / ...
	#----------------------------------
	
	@staticmethod
	def add(a: Any, b: Any) -> np.generic | np.ndarray:
		try:
			result = np.add(a, b)
		except Exception as e:
			raise excp.InputError(f"`a` and `b` can't be added") from e
			
		if isinstance(a, str) and isinstance(b, str): # numpy actually concatenates, we do not want that
			raise excp.InputError(f"`a` and `b` can't be added")
		return result
	
	@staticmethod
	def subtract(a: Any, b: Any) -> np.generic | np.ndarray:
		try:
			result = np.subtract(a, b)
		except Exception as e:
			raise excp.InputError(f"`a` and `b` can't be subtracted") from e
		return result
		
	@staticmethod
	def multiply(a: Any, b: Any) -> np.generic | np.ndarray:
		try:
			result = np.multiply(a, b)
		except Exception as e:
			raise excp.InputError(f"`a` and `b` can't be multiplied") from e
		
		if isinstance(a, str) and isinstance(b, str): # numpy actually concatenates, we do not want that
			raise excp.InputError(f"`a` and `b` can't be multiplied")
		return result

	@staticmethod
	def divide(a: Any, b: Any) -> np.generic | np.ndarray:
		try:
			result = np.divide(a, b)
		except Exception as e:
			raise excp.InputError(f"`a` and `b` can't be divided") from e
		return result

	@staticmethod
	def power(a: Any, b: Any) -> np.generic | np.ndarray:
		try:
			result = np.power(a, b)
		except Exception as e:
			raise excp.InputError(f"`a` can't be exponentiated with `b`") from e
		return result
	
	@staticmethod
	def floor_divide(a: Any, b: Any) -> np.generic | np.ndarray:
		try:
			result = np.floor_divide(a, b)
		except Exception as e:
			raise excp.InputError(f"`a` can't be floor divided by `b`") from e
		return result
		
	#----------------------------------
	# To handle numpy aggregator ops
	#----------------------------------
	@staticmethod
	def mean(a: Any, axis: int | None = None) -> np.generic | np.ndarray:
		try:
			result = np.mean(a, axis=axis)
		except Exception as e:
			raise excp.InputError(f"can't find mean for `a`") from e
		return result
	
	@staticmethod
	def std(a: Any, axis: int | None = None) -> np.generic | np.ndarray:
		""""""
		try:
			result = np.std(a, axis=axis)
		except Exception as e:
			raise excp.InputError(f"can't find std for `a`") from e
		return result
	
	@staticmethod
	def min(a: Any, axis: int | None = None) -> np.generic | np.ndarray:
		try:
			result = np.min(a, axis=axis)
		except Exception as e:
			raise excp.InputError(f"can't find min for `a`") from e
		return result
	
	@staticmethod
	def max(a: Any, axis: int | None = None) -> np.generic | np.ndarray:
		try:
			result = np.max(a, axis=axis)
		except Exception as e:
			raise excp.InputError(f"can't find max for `a`") from e
		return result
	
	@staticmethod
	def sum(a: Any, axis: int | None = None) -> np.generic | np.ndarray:
		try:
			result = np.sum(a, axis=axis)
		except Exception as e:
			raise excp.InputError(f"can't find sum for `a`") from e
		return result
	
	#----------------------------------
	# To handle numpy ops where the
	# shapes are unaltered
	# sin, cos, exp, log, ...
	#----------------------------------
	
	@staticmethod
	def sin(a: Any) -> np.generic | np.ndarray:
		try:
			result = np.sin(a)
		except Exception as e:
			raise excp.InputError(f"can't find sin for `a`") from e
		return result
	
	@staticmethod
	def cos(a: Any) -> np.generic | np.ndarray:
		try:
			result = np.cos(a)
		except Exception as e:
			raise excp.InputError(f"can't find cos for `a`") from e
		return result
	
	@staticmethod
	def tanh(a: Any) -> np.generic | np.ndarray:
		try:
			result = np.tanh(a)
		except Exception as e:
			raise excp.InputError(f"can't find tanh for `a`") from e
		return result
	
	@staticmethod
	def exp(a: Any) -> np.generic | np.ndarray:
		try:
			result = np.exp(a)
		except Exception as e:
			raise excp.InputError(f"can't find exp for `a`") from e
		return result
	
	@staticmethod
	def log(a: Any) -> np.generic | np.ndarray:
		try:
			result = np.log(a)
		except Exception as e:
			raise excp.InputError(f"can't find log for `a`") from e
		return result
	
	@staticmethod
	def log10(a: Any) -> np.generic | np.ndarray:
		try:
			result = np.log10(a)
		except Exception as e:
			raise excp.InputError(f"can't find log10 for `a`") from e
		return result
	
	@staticmethod
	def log2(a: Any) -> np.generic | np.ndarray:
		try:
			result = np.log2(a)
		except Exception as e:
			raise excp.InputError(f"can't find log2 for `a`") from e
		return result
	
	@staticmethod
	def log1p(a: Any) -> np.generic | np.ndarray:
		try:
			result = np.log1p(a)
		except Exception as e:
			raise excp.InputError(f"can't find log1p for `a`") from e
		return result
	
	
	@staticmethod
	def sqrt(a: Any) -> np.generic | np.ndarray:
		try:
			result = np.sqrt(a)
		except Exception as e:
			raise excp.InputError(f"can't find sqrt for `a`") from e
		return result
	
	@staticmethod
	def abs(a: Any) -> np.generic | np.ndarray:
		try:
			result = np.abs(a)
		except Exception as e:
			raise excp.InputError(f"can't find abs for `a`") from e
		return result
	
	@staticmethod
	def floor(a: Any) -> np.generic | np.ndarray:
		try:
			result = np.floor(a)
		except Exception as e:
			raise excp.InputError(f"can't find floor for `a`") from e
		return result
	
	@staticmethod
	def ceil(a: Any) -> np.generic | np.ndarray:
		try:
			result = np.ceil(a)
		except Exception as e:
			raise excp.InputError(f"can't find ceil for `a`") from e
		return result
	
	@staticmethod
	def round(a: Any) -> np.generic | np.ndarray:
		try:
			result = np.round(a)
		except Exception as e:
			raise excp.InputError(f"can't find round for `a`") from e
		return result
	
	#------------------------------------
	# TODO: Add shape-changing ops like 
	# reshape, transpose, squeeze later
	#------------------------------------
	
	@staticmethod
	def reshape(a: Any, shape: int | tuple[int, ...]) -> np.ndarray:
		try:
			result = np.reshape(a, shape=shape)
		except Exception as e:
			raise excp.InputError(f"can't reshape `a`") from e
		return result
	
	#------------------------------------
	# Complex numbers operations
	#------------------------------------
	
	@staticmethod
	def real(a: Any) -> np.ndarray:
		try:
			result = np.real(a)
		except Exception as e:
			raise excp.InputError(f"can't find real for `a`") from e
		return result
	
	@staticmethod
	def imag(a: Any) -> np.ndarray:
		try:
			result = np.imag(a)
		except Exception as e:
			raise excp.InputError(f"can't find imag for `a`") from e
		return result
	
	@staticmethod
	def angle(a: Any) -> np.ndarray:
		try:
			result = np.angle(a)
		except Exception as e:
			raise excp.InputError(f"can't find angle for `a`") from e
		return result
	
	#------------------------------------
	# Comparison
	#------------------------------------
	
	@staticmethod
	def lt(a: Any, b: Any) -> np.ndarray:
		try:
			mask = a < b
		except Exception as e:
			raise excp.InputError(f"`a` and `b` can't be compared") from e
		return mask
	
	@staticmethod
	def le(a: Any, b: Any) -> np.ndarray:
		try:
			mask = a <= b
		except Exception as e:
			raise excp.InputError(f"`a` and `b` can't be compared") from e
		return mask
	
	@staticmethod
	def gt(a: Any, b: Any) -> np.ndarray:
		try:
			mask = a > b
		except Exception as e:
			raise excp.InputError(f"`a` and `b` can't be compared") from e
		return mask
	
	@staticmethod
	def ge(a: Any, b: Any) -> np.ndarray:
		try:
			mask = a >= b
		except Exception as e:
			raise excp.InputError(f"`a` and `b` can't be compared") from e
		return mask
	
	@staticmethod
	def eq(a: Any, b: Any) -> np.ndarray:
		try:
			mask = a == b
		except Exception as e:
			raise excp.InputError(f"`a` and `b` can't be compared") from e
		return mask
	
	@staticmethod
	def ne(a: Any, b: Any) -> np.ndarray:
		try:
			mask = a != b
		except Exception as e:
			raise excp.InputError(f"`a` and `b` can't be compared") from e
		return mask