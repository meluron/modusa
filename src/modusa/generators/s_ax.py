#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import validate_args_type
from .base import ModusaGenerator
from modusa.models.s_ax import SAx
import numpy as np

class SAxGen(ModusaGenerator):
	"""
	Provides user friendly APIs to generate axis for
	signals (instances of `SAx`).
	"""
	
	#--------Meta Information----------
	_name = "SignalAxisGenerator"
	_description = "APIs to generate axis for signals."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-25"
	#----------------------------------
	
	
	@classmethod
	@validate_args_type()
	def from_array(
		cls,
		values: np.ndarray | list | float | int | np.generic,
		label: str = "SAx"
	) -> SAx:
		"""
		Create `SAx` instance from basic data structures.
		
		.. code-block:: python

			import modusa as ms
			x = ms.sax.from_array([1, 2, 3])
			print(x)
			time_sax.print_info()

		Parameters
		----------
		values: np.ndarray | list | float | int | np.generic
			- The values for the axis.
		label: str
			- Label for the axis.

		Returns
		-------
		SAx
			An instance of SAx.
		"""
		
		if isinstance(values, (int, float, np.generic)): values = [values] # Scalar to 1D
		values = np.asarray(values)

		return SAx(values=values, label=label)
		
	
	@classmethod
	def linear(cls, n_points: int, sr: int | float = 1.0, start: int | float = 0.0, label: str = "Linear Axis") -> SAx:
		"""
		Create a linearly spaced axis.
		
		.. code-block:: python

			import modusa as ms
			x = ms.sax.linear(n_points=100, sr=2, start=10, label="Time (sec)")
			print(x)
			x.print_info()
		
		Parameters
		----------
		n_points: int
			- Number of data points for the axis.
		sr: int | float
			- Sampling rate of the axis.
		start: int | float
			- Start value.
		label: str
			- Label for the axis.
		
		Returns
		-------
		SAx
			An instance of SAx.
		"""
		
		assert isinstance(n_points, int)
		assert isinstance(sr, (int, float))
		assert isinstance(start, (int, float))
		assert isinstance(label, str)
	
		sr = float(sr)
		start = float(start)
	
		values = start + np.arange(n_points) / sr  # ensures exact number of points
		time_ax = SAx(values=values, label=label)
		time_ax.sr = sr
	
		return time_ax