#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import validate_args_type
from .base import ModusaGenerator
from modusa.models.s2d import S2D
from modusa.models.s_ax import SAx
from modusa.models.data import Data
import numpy as np

class S2DGen(ModusaGenerator):
	"""
	Provides user friendly APIs to generate instances of different `S2D`
	instances.
	"""
	
	#--------Meta Information----------
	_name = "S2DGeneratator"
	_description = "APIs to generate instances of different `S2D` instances"
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-27"
	#----------------------------------
	
	@staticmethod
	def from_array(
		M: np.ndarray | list | float | int | np.generic,
		y: np.ndarray | list | float | int | np.generic | None = None,
		x: np.ndarray | list | float | int | np.generic | None = None,
		M_label: str = "M",
		y_label: str = "Y",
		x_label: str = "X",
		title: str = "2D Signal"
	) -> S2D:
		"""
		Create `S2D` instance from basic data structures.

		.. code-block:: python

			import modusa as ms
			M = ms.s1d.from_array([1, 2, 3])
			print(M)
			M.print_info()
		
		Parameters
		----------
		M: np.ndarray | list | float | int | np.generic
			- Data values.
		y: np.ndarray | list | float | int | np.generic
			- y axis values.
			- Default: None → Creates an integer indexing.
		x: np.ndarray | list | float | int | np.generic | None
			- x axis values.
			- Default: None → Creates an integer indexing.
		M_label: str
			- Label for the data.
			- Default: "M"
		y_label: str
			- Y label for the signal.
			- Default: "Y"
		x_label: str
			- X label for the signal.
			- Default: "X"
		title: str
			- Title for the signal.
			- Default: "2D Signal"
		Returns
		-------
		S2D
			An instance of S2D.
		"""
		assert isinstance(M, (np.ndarray, list, float, int, np.generic))
		assert isinstance(x, (np.ndarray, list, float, int, np.generic)) or x is None
		assert isinstance(y, (np.ndarray, list, float, int, np.generic)) or y is None
		assert isinstance(M_label, str) and isinstance(y_label, str) and isinstance(x_label, str) and isinstance(title, str)
		
		if isinstance(M, (float, int, np.generic)): M = [[M]] # Convert to list of 1 element
		if isinstance(y, (float, int, np.generic)): y = [y] # Convert to list of 1 element
		if isinstance(x, (float, int, np.generic)): x = [x] # Convert to list of 1 element
		
		M = np.asarray(M)
		assert M.ndim == 2
		
		if y is None: y = np.arange(M.shape[0])
		else: y = np.asarray(y)
		assert y.ndim == 1
		
		if x is None: x = np.arange(M.shape[1])
		else: x = np.asarray(x)
		assert x.ndim == 1
		
		assert y.shape[0] == M.shape[0], "Shape mismatch"
		assert x.shape[0] == M.shape[1], "Shape mismatch"
		
		y_sax = SAx(values=y, label=y_label) # Creating a signal axis instance
		x_sax = SAx(values=x, label=x_label) # Creating a signal axis instance
		
		M = Data(values=M, label=M_label)
		
		return S2D(M=M, y=y_sax, x=x_sax, title=title)
	
	@classmethod
	def zeros(cls, shape: tuple[int, int]) -> S2D:
		"""
		Create `S2D` instance with all zeros.

		.. code-block:: python

			import modusa as ms
			M = ms.s2d.zeros((10, 5))
			print(M)
			M.print_info()
		
		Parameters
		----------
		shape: tuple[int, int]
			- Shape of the signal with zeros.
			- Must be 1 dimensional
			- E.g. (10, 5)
		Returns
		-------
		S2D
			An instance of S2D.
		"""
		assert isinstance(shape, tuple)
		M = np.zeros(shape)
		
		return cls.from_array(M=M, title="Zeros")
	
	@classmethod
	def zeros_like(cls, signal: S2D) -> S2D:
		"""
		Create `S2D` instance similar to `signal`
		but with all entries being zeros.

		.. code-block:: python

			import modusa as ms
			signal = ms.s2d.from_array([[1, 2, 3], [4, 5, 6]])
			M = ms.s2d.zeros_like(signal)
			print(M)
			M.print_info()
		
		Parameters
		----------
		signal: S2D
			- Reference signal to create zeros like that.
		Returns
		-------
		S2D
			An instance of S2D.
		"""
		
		assert signal.__class__ in [S2D]
		
		M = np.zeros(signal.shape)
		y = signal._y
		x = signal._x
		
		M_label = signal._M_label
		y_label = signal._y_label
		x_label = signal._x_label
		title = signal._title
		
		return cls.from_array(M=M, y=y, x=x, M_label=M_label, y_label=y_label, x_label=x_label, title=title)
	
	
	@classmethod
	def ones(cls, shape: tuple[int, int]) -> S2D:
		"""
		Create `S2D` instance with all ones.

		.. code-block:: python

			import modusa as ms
			M = ms.s2d.ones((10, 5))
			print(M)
			M.print_info()
		
		Parameters
		----------
		shape: tuple[int, int]
			- Shape of the signal with ones.
			- Must be 1 dimensional
			- E.g. (10, 5)
		Returns
		-------
		S2D
			An instance of S2D.
		"""
		assert isinstance(shape, tuple)
		M = np.ones(shape)
		
		return cls.from_array(M=M, title="Ones")
	
	@classmethod
	def ones_like(cls, signal: S2D) -> S2D:
		"""
		Create `S2D` instance similar to `signal`
		but with all entries being ones.

		.. code-block:: python

			import modusa as ms
			signal = ms.s2d.from_array([[1, 2, 3], [4, 5, 6]])
			M = ms.s2d.ones_like(signal)
			print(M)
			M.print_info()
		
		Parameters
		----------
		signal: S2D
			- Reference signal to create ones like that.
		Returns
		-------
		S2D
			An instance of S2D.
		"""
		
		assert signal.__class__ in [S2D]
		
		M = np.ones(signal.shape)
		y = signal._y
		x = signal._x
		
		M_label = signal._M_label
		y_label = signal._y_label
		x_label = signal._x_label
		title = signal._title
		
		return cls.from_array(M=M, y=y, x=x, M_label=M_label, y_label=y_label, x_label=x_label, title=title)
	
	@classmethod
	def random(cls, shape: tuple[int, int]) -> S2D:
		"""
		Create `S2D` instance with random entries.

		.. code-block:: python

			import modusa as ms
			y = ms.s2d.random((10, 5))
			print(y)
			y.print_info()
		
		Parameters
		----------
		shape: tuple[int, int]
			- Shape of the signal.
			- Must be 1 dimensional
			- E.g. (10, 5)
		Returns
		-------
		S2D
			An instance of S2D with random values.
		"""
		assert isinstance(shape, tuple)
		M = np.random.random(shape)
		
		return cls.from_array(M=M, title="Random")
	
	@classmethod
	def random_like(cls, signal: S2D) -> S2D:
		"""
		Create `S2D` instance similar to `signal`
		but with all entries being ones.

		.. code-block:: python

			import modusa as ms
			signal = ms.s2d.from_array([[1, 2, 3], [4, 5, 6]])
			M = ms.s2d.random_like(signal)
			print(M)
			M.print_info()
		
		Parameters
		----------
		signal: S2D
			- Reference signal.
		Returns
		-------
		S2D
			An instance of S2D with random values.
		"""
		
		assert signal.__class__ in [S2D]
		
		M = np.random.random(signal.shape)
		y = signal._y
		x = signal._x
		
		M_label = signal._M_label
		y_label = signal._y_label
		x_label = signal._x_label
		title = signal._title
		
		return cls.from_array(M=M, y=y, x=x, M_label=M_label, y_label=y_label, x_label=x_label, title=title)
	
	
	