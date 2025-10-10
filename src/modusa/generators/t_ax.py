#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import validate_args_type
from modusa.generators.base import ModusaGenerator
from modusa.models.t_ax import TAx
import numpy as np

class TAxGen(ModusaGenerator):
	"""
	Provides user friendly APIs to generate time
	axis for signals (instances of `TAx`).
	"""
	
	#--------Meta Information----------
	_name = "TimeAxisGenerator"
	_description = "APIs to generate time axis for signals."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-26"
	#----------------------------------
		
	@classmethod
	def linear(cls, n_points: int, sr: int | float = 1.0, t0: int | float = 0.0, label: str = "Time (sec)") -> TAx:
		"""
		Create a linearly spaced time axis.
		
		.. code-block:: python

			import modusa as ms
			t = ms.tax.linear(n_points=100, sr=2, start=10, label="Time (sec)")
			print(t)
			t.print_info()
		
		Parameters
		----------
		n_points: int
			- Number of data points for the time axis.
		sr: int | float
			- Sampling rate for the time axis.
		start: int | float
			- Start value.
		label: str
			- Label for the time axis.
		
		Returns
		-------
		TAx
			An instance of TAx.
		"""
		
		assert isinstance(n_points, int)
		assert isinstance(sr, (int, float))
		assert isinstance(t0, (int, float))
		assert isinstance(label, str)
		
		sr = float(sr)
		t0 = float(t0)
		
		time_ax = TAx(n_points=n_points, sr=sr, t0=t0, label=label)
		
		return time_ax
	