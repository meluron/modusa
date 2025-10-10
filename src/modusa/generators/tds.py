#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import validate_args_type
from .base import ModusaGenerator
from modusa.models.tds import TDS
from modusa.models.t_ax import TAx
from modusa.models.data import Data
import numpy as np

class TDSGen(ModusaGenerator):
	"""
	Provides user friendly APIs to generate instances of different 
	`TDS` instances.
	"""
	
	#--------Meta Information----------
	_name = "TDSGenerator"
	_description = ""
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-27"
	#----------------------------------
	
	@staticmethod
	def from_array(
		y: np.ndarray | list | float | int | np.generic,
		sr: float | int = 1.0,
		t0: float | int = 0.0,
		y_label: str = "Y",
		t_label: str = "Time (sec)",
		title: str = "Time Domain Signal"
	) -> TDS:
		"""
		Create `TDS` instance from basic data structures.

		.. code-block:: python

			import modusa as ms
			t = ms.tds.from_array([1, 2, 3])
			print(t)
			t.print_info()
		
		Parameters
		----------
		y: np.ndarray | list | float | int | np.generic
			- Data values.
		sr: float | int
			- Sampling rate.
		t0: float | int
			- Start timestamp.
		y_label: str
			- Y label for the signal.
			- Default: "Y"
		t_label: str
			- T label for the signal.
			- Default: "Time (sec)"
		title: str
			- Title for the signal.
			- Default: "1D Signal"
		Returns
		-------
		TDS
			An instance of TDS.
		"""
		assert isinstance(y, (np.ndarray, list, float, int, np.generic))
		assert isinstance(sr, (int, float)) and isinstance(t0, (int, float))
		assert isinstance(y_label, str) and isinstance(t_label, str) and isinstance(title, str)
		
		if isinstance(y, (float, int, np.generic)): y = [y] # Convert to list of 1 element
		y = np.asarray(y)
		assert y.ndim == 1
		
		sr = float(sr)
		t0 = float(t0)
		
		y = Data(values=y, label=y_label)
		t = TAx(n_points=y.shape[0], sr=sr, t0=t0, label=t_label) # Creating a signal axis instance
		
		return TDS(y=y, t=t, title=title)
	
	@classmethod
	def zeros(cls, shape, sr=1.0, t0=0.0) -> TDS:
		"""
		Create `TDS` instance with all zeros.

		.. code-block:: python

			import modusa as ms
			y = ms.tds.zeros(10, sr=10)
			print(y)
			y.print_info()
		
		Parameters
		----------
		shape: int | tuple[int]
			- Shape of the signal with zeros.
			- Must be 1 dimensional
			- E.g. 10 or (10, )
		sr: float | int
			- Sampling rate.
		t0: float | int
			- Start timestamp.
		Returns
		-------
		TDS
			An instance of TDS.
		"""
		assert isinstance(shape, (int, tuple))
		y = np.zeros(shape)
		
		return cls.from_array(y=y, sr=sr, t0=t0, title="Zeros")
	
	@classmethod
	def zeros_like(cls, signal, shape=None) -> TDS:
		"""
		Create `TDS` instance similar to `signal`
		but with all entries being zeros.

		.. code-block:: python

			import modusa as ms
			signal = ms.tds.from_array([1, 2, 3])
			y = ms.tds.zeros_like(signal)
			print(y)
			x.print_info()
		
		Parameters
		----------
		signal: TDS
			- Reference signal to create zeros like that.
		Returns
		-------
		TDS
			An instance of TDS.
		"""
		
		assert isinstance(signal, TDS)
		
		shape = signal.shape if shape is None else shape
		
		return cls.from_array(y=np.zeros(shape), sr=signal.t.sr, t0=signal.t.t0, y_label=signal.y.label, t_label=signal.t.label, title=signal.title)
	
	
	@classmethod
	def ones(cls, shape, sr=1.0, t0=0.0) -> TDS:
		"""
		Create `TDS` instance with all ones.

		.. code-block:: python

			import modusa as ms
			y = ms.tds.ones(10)
			print(y)
			y.print_info()
		
		Parameters
		----------
		shape: int | tuple[int]
			- Shape of the signal with ones.
			- Must be 1 dimensional
			- E.g. 10 or (10, )
		sr: float | int
			- Sampling rate.
		t0: float | int
			- Start timestamp.
		Returns
		-------
		TDS
			An instance of TDS.
		"""
		assert isinstance(shape, (int, tuple))
		y = np.ones(shape)
		
		return cls.from_array(y=y, sr=sr, t0=t0, title="Ones")
	
	@classmethod
	def ones_like(cls, signal, shape=None) -> TDS:
		"""
		Create `TDS` instance similar to `signal`
		but with all entries being ones.
		
		.. code-block:: python

			import modusa as ms
			signal = ms.tds.from_array([1, 2, 3])
			y = ms.tds.ones_like(signal)
			print(y)
			y.print_info()
		
		Parameters
		----------
		signal: TDS
			- Reference signal to create ones like that.
		Returns
		-------
		TDS
			An instance of TDS.
		"""
		assert isinstance(signal, TDS)
		
		shape = signal.shape if shape is None else shape
		
		return cls.from_array(y=np.ones(shape), sr=signal.t.sr, t0=signal.t.t0, y_label=signal.y.label, t_label=signal.t.label, title=signal.title)
	
	@classmethod
	def random(cls, shape, sr=1.0, t0=0.0) -> TDS:
		"""
		Create `TDS` instance with random entries.

		.. code-block:: python

			import modusa as ms
			x = ms.tds.random(10)
			print(x)
			x.print_info()
		
		Parameters
		----------
		shape: int | tuple[int]
			- Shape of the signal.
			- Must be 1 dimensional
			- E.g. 10 or (10, )
		sr: float | int
			- Sampling rate.
		t0: float | int
			- Start timestamp.
		Returns
		-------
		TDS
			An instance of TDS with random values.
		"""
		assert isinstance(shape, (int, tuple))
		y = np.random.random(shape)
		
		return cls.from_array(y=y, sr=sr, t0=t0, title="Random")
	
	@classmethod
	def random_like(cls, signal, shape=None) -> TDS:
		"""
		Create `TDS` instance similar to `signal`
		but with all entries being ones.

		.. code-block:: python

			import modusa as ms
			signal = ms.tds.from_array([1, 2, 3])
			y = ms.tds.random_like(signal)
			print(y)
			y.print_info()
		
		Parameters
		----------
		signal: TDS
			- Reference signal to create one with random entries.
		Returns
		-------
		TDS
			An instance of TDS with random values.
		"""
		assert isinstance(signal, TDS)
		
		shape = signal.shape if shape is None else shape
		
		return cls.from_array(y=np.random.random(shape), sr=signal.t.sr, t0=signal.t.t0, y_label=signal.y.label, t_label=signal.t.label, title=signal.title)
	