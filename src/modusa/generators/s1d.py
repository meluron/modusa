#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import validate_args_type
from .base import ModusaGenerator
from modusa.models.s1d import S1D
from modusa.models.s_ax import SAx
from modusa.models.data import Data
import numpy as np

class S1DGen(ModusaGenerator):
	"""
	Provides user friendly APIs to generate instances of different `S1D`
	instances.
	"""
	
	#--------Meta Information----------
	_name = ""
	_description = ""
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-27"
	#----------------------------------
	
	@staticmethod
	def from_array(
		y,
		x = None,
		y_label: str = "Y",
		x_label: str = "X",
		title: str = "1D Signal"
	) -> S1D:
		"""
		Create `S1D` instance from basic data structures.

		.. code-block:: python

			import modusa as ms
			x = ms.s1d.from_array([1, 2, 3])
			print(x)
			x.print_info()
		
		Parameters
		----------
		y: array-like
			- Data values.
		x: array-like | None
			- Corresponding axis values.
			- Default: None → Creates an integer indexing.
		y_label: str
			- Y label for the signal.
			- Default: "Y"
		x_label: str
			- X label for the signal.
			- Default: "X"
		title: str
			- Title for the signal.
			- Default: "1D Signal"
		Returns
		-------
		S1D
			An instance of S1D.
		"""
		assert isinstance(y, (np.ndarray, list, float, int, np.generic))
		assert isinstance(x, (np.ndarray, list, float, int, np.generic)) or x is None
		assert isinstance(y_label, str) and isinstance(x_label, str) and isinstance(title, str)
		
		if isinstance(y, (float, int, np.generic)): y = [y] # Convert to list of 1 element
		if isinstance(x, (float, int, np.generic)): x = [x] # Convert to list of 1 element
		
		y = np.asarray(y)
		if x is None: x = np.arange(y.shape[0])
		else: x = np.asarray(x)
		
		assert y.ndim ==1 and x.ndim == 1, "S1D must have only one dimension"
		assert y.shape == x.shape, "Shape mismatch"
		
		y = Data(values=y, label=y_label)
		x = SAx(values=x, label=x_label) # Creating a signal axis instance
		
		return S1D(y=y, x=x, title=title)
	
	@classmethod
	def zeros(cls, shape) -> S1D:
		"""
		Create `S1D` instance with all zeros.

		.. code-block:: python

			import modusa as ms
			y = ms.s1d.zeros(10)
			print(y)
			y.print_info()
		
		Parameters
		----------
		shape: int | tuple[int]
			- Shape of the signal with zeros.
			- Must be 1 dimensional
			- E.g. 10 or (10, )
		Returns
		-------
		S1D
			An instance of S1D.
		"""
		assert isinstance(shape, (int, tuple))
		y = np.zeros(shape)
		
		return cls.from_array(y=y, title="Zeros")
	
	@classmethod
	def zeros_like(cls, signal: S1D) -> S1D:
		"""
		Create `S1D` instance similar to `signal`
		but with all entries being zeros.

		.. code-block:: python

			import modusa as ms
			signal = ms.s1d.from_array([1, 2, 3])
			y = ms.s1d.zeros_like(signal)
			print(y)
			x.print_info()
		
		Parameters
		----------
		signal: S1D
			- Reference signal to create zeros like that.
		Returns
		-------
		S1D
			An instance of S1D.
		"""
		
		assert signal.__class__ in [S1D]
		
		y = np.zeros(signal.shape)
		y_label = signal._y_label
		x = signal._x
		x_label = signal._x_label
		title = signal._title
		
		return cls.from_array(y=y, x=x, y_label=y_label, x_label=x_label, title=title)
	
	
	@classmethod
	def ones(cls, shape: int | tuple[int, int]) -> S1D:
		"""
		Create `S1D` instance with all ones.

		.. code-block:: python

			import modusa as ms
			y = ms.s1d.ones(10)
			print(y)
			y.print_info()
		
		Parameters
		----------
		shape: int | tuple[int]
			- Shape of the signal with ones.
			- Must be 1 dimensional
			- E.g. 10 or (10, )
		Returns
		-------
		S1D
			An instance of S1D.
		"""
		assert isinstance(shape, (int, tuple))
		y = np.ones(shape)
		
		return cls.from_array(y=y, title="Ones")
	
	@classmethod
	def ones_like(cls, signal: S1D) -> S1D:
		"""
		Create `S1D` instance similar to `signal`
		but with all entries being ones.

		.. code-block:: python

			import modusa as ms
			signal = ms.s1d.from_array([1, 2, 3])
			y = ms.s1d.ones_like(signal)
			print(y)
			y.print_info()
		
		Parameters
		----------
		signal: S1D
			- Reference signal to create ones like that.
		Returns
		-------
		S1D
			An instance of S1D.
		"""
		
		assert signal.__class__ in [S1D]
		
		y = np.ones(signal.shape)
		y_label = signal._y_label
		x = signal._x
		x_label = signal._x_label
		title = signal._title
		
		return cls.from_array(y=y, x=x, y_label=y_label, x_label=x_label, title=title)
	
	@classmethod
	def random(cls, shape: int) -> S1D:
		"""
		Create `S1D` instance with random entries.

		.. code-block:: python

			import modusa as ms
			y = ms.s1d.random(10)
			print(y)
			y.print_info()
		
		Parameters
		----------
		shape: int | tuple[int]
			- Shape of the signal.
			- Must be 1 dimensional
			- E.g. 10 or (10, )
		Returns
		-------
		S1D
			An instance of S1D with random values.
		"""
		assert isinstance(shape, (int, tuple))
		y = np.random.random(shape)
		
		return cls.from_array(y=y, title="Random")
	
	@classmethod
	def random_like(cls, signal: S1D) -> S1D:
		"""
		Create `S1D` instance similar to `signal`
		but with all entries being ones.

		.. code-block:: python

			import modusa as ms
			signal = ms.s1d.from_array([1, 2, 3])
			y = ms.s1d.random_like(signal)
			print(y)
			y.print_info()
		
		Parameters
		----------
		signal: S1D
			- Reference signal to create one with random entries.
		Returns
		-------
		S1D
			An instance of S1D with random values.
		"""
		
		assert signal.__class__ in [S1D]
		
		y = np.random.random(signal.shape)
		y_label = signal._y_label
		x = signal._x
		x_label = signal._x_label
		title = signal._title
		
		return cls.from_array(y=y, x=x, y_label=y_label, x_label=x_label, title=title)
	