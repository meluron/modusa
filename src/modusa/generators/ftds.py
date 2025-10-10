#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import validate_args_type
from .base import ModusaGenerator
from modusa.models.data import Data
from modusa.models.s_ax import SAx
from modusa.models.t_ax import TAx
from modusa.models.ftds import FTDS
import numpy as np

class FTDSGen(ModusaGenerator):
	"""
	Provides user friendly APIs to generate instances of different 
	`FTDS` instances.
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
		M: np.ndarray | list | float | int | np.generic,
		f: np.ndarray | list | float | int | np.generic | None = None,
		sr: int | float = 1.0,
		t0: int | float = 0.0,
		M_label: str = "M",
		f_label: str = "Feature",
		t_label: str = "Time (sec)",
		title: str = "Feature Time Domain Signal"
	) -> FTDS:
		"""
		Create `FDTS` instance from basic data structures.

		.. code-block:: python

			import modusa as ms
			M = ms.ftds.from_array([1, 2, 3])
			print(M)
			M.print_info()
		
		Parameters
		----------
		M: np.ndarray | list | float | int | np.generic
			- Data values.
		f: np.ndarray | list | float | int | np.generic | None
			- y axis values.
			- Default: None → Creates an integer indexing.
		sr: int | float
			- Sampling rate / Frame rate.
			- Default: 1.0
		t0: int | float
			- Start timestamp.
			- Default: 0.0
		M_label: str
			- Label for the data.
			- Default: "M"
		f_label: str
			- Feature label for the signal.
			- Default: "Feature"
		t_label: str
			- Time label for the signal.
			- Default: "Time (sec)"
		title: str
			- Title for the signal.
			- Default: "Feature Time Domain Signal"
		Returns
		-------
		FTDS
			An instance of FTDS.
		"""
		assert isinstance(M, (np.ndarray, list, float, int, np.generic))
		assert isinstance(f, (np.ndarray, list, float, int, np.generic)) or f is None
		assert isinstance(sr, (int, float)) and isinstance(t0, (int, float))
		assert isinstance(M_label, str) and isinstance(f_label, str) and isinstance(t_label, str) and isinstance(title, str)
		
		if isinstance(M, (float, int, np.generic)): M = [[M]] # Convert to list of 1 element
		if isinstance(f, (float, int, np.generic)): f = [f] # Convert to list of 1 element
		
		M = np.asarray(M)
		assert M.ndim == 2
		
		if f is None: f = np.arange(M.shape[0])
		else: f = np.asarray(f)
		assert f.ndim == 1
		assert f.shape[0] == M.shape[0], "Shape mismatch"
		
		sr = float(sr)
		t0 = float(t0)
		
		M = Data(values=M, label=M_label)
		f = SAx(values=f, label=f_label)
		t = TAx(n_points=M.shape[1], sr=sr, t0=t0, label=t_label)
		
		return FTDS(M=M, f=f, t=t, title=title)
	
	@classmethod
	def zeros(cls, shape, f=None, sr=1.0, t0=0.0) -> FTDS:
		"""
		Create `FTDS` instance with all zeros.

		.. code-block:: python

			import modusa as ms
			M = ms.ftds.zeros((10, 5))
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
		FTDS
			An instance of FTDS.
		"""
		assert isinstance(shape, tuple)
		M = np.zeros(shape)
		
		return cls.from_array(M=M, f=f, sr=sr, t0=t0, title="Zeros")
	
	@classmethod
	def zeros_like(cls, signal: FTDS) -> FTDS:
		"""
		Create `FTDS` instance similar to `signal`
		but with all entries being zeros.

		.. code-block:: python

			import modusa as ms
			signal = ms.ftds.from_array([[1, 2, 3], [4, 5, 6]])
			M = ms.ftds.zeros_like(signal)
			print(M)
			M.print_info()
		
		Parameters
		----------
		signal: FTDS
			- Reference signal to create zeros like that.
		Returns
		-------
		FTDS
			An instance of FTDS.
		"""
		
		assert signal.__class__ in [FTDS]
		
		M = np.zeros(signal.shape)
		f = signal._f
		t = signal._t
		
		M_label = signal._M_label
		f_label = signal._f_label
		t_label = signal._t_label
		title = signal._title
		
		return cls.from_array(M=M, f=f, t=t, M_label=M_label, f_label=f_label, t_label=t_label, title=title)
	
	
	@classmethod
	def ones(cls, shape: tuple[int, int]) -> FTDS:
		"""
		Create `FTDS` instance with all ones.

		.. code-block:: python

			import modusa as ms
			M = ms.ftds.ones((10, 5))
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
		FTDS
			An instance of FTDS.
		"""
		assert isinstance(shape, tuple)
		M = np.ones(shape)
		
		return cls.from_array(M=M, title="Ones")
	
	@classmethod
	def ones_like(cls, signal: FTDS) -> FTDS:
		"""
		Create `FTDS` instance similar to `signal`
		but with all entries being ones.

		.. code-block:: python

			import modusa as ms
			signal = ms.ftds.from_array([[1, 2, 3], [4, 5, 6]])
			M = ms.ftds.ones_like(signal)
			print(M)
			M.print_info()
		
		Parameters
		----------
		signal: FTDS
			- Reference signal to create ones like that.
		Returns
		-------
		FTDS
			An instance of FTDS.
		"""
		
		assert signal.__class__ in [FTDS]
		
		M = np.ones(signal.shape)
		f = signal._f
		t = signal._t
		
		M_label = signal._M_label
		f_label = signal._f_label
		t_label = signal._t_label
		title = signal._title
		
		return cls.from_array(M=M, f=f, t=t, M_label=M_label, f_label=f_label, t_label=t_label, title=title)
	
	@classmethod
	def random(cls, shape: tuple[int, int]) -> FTDS:
		"""
		Create `FTDS` instance with random entries.

		.. code-block:: python

			import modusa as ms
			M = ms.ftds.random((10, 5))
			print(M)
			M.print_info()
		
		Parameters
		----------
		shape: tuple[int, int]
			- Shape of the signal with random values.
			- Must be 1 dimensional
			- E.g. (10, 5)
		Returns
		-------
		FTDS
			An instance of FTDS.
		"""
		assert isinstance(shape, tuple)
		M = np.random.random(shape)
		
		return cls.from_array(M=M, title="Random")
	
	@classmethod
	def random_like(cls, signal: FTDS) -> FTDS:
		"""
		Create `FTDS` instance similar to `signal`
		but with random entries.

		.. code-block:: python

			import modusa as ms
			signal = ms.ftds.from_array([[1, 2, 3], [4, 5, 6]])
			M = ms.ftds.random_like(signal)
			print(M)
			M.print_info()
		
		Parameters
		----------
		signal: FTDS
			- Reference signal.
		Returns
		-------
		FTDS
			An instance of FTDS with random values.
		"""
		
		assert signal.__class__ in [FTDS]
		
		M = np.random.random(signal.shape)
		f = signal._f
		t = signal._t
		
		M_label = signal._M_label
		f_label = signal._f_label
		t_label = signal._t_label
		title = signal._title
		
		return cls.from_array(M=M, f=f, t=t, M_label=M_label, f_label=f_label, t_label=t_label, title=title)
	