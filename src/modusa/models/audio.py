#!/usr/bin/env python3

from modusa import excp
from modusa.decorators import immutable_property, validate_args_type
from .tds import TDS
from .data import Data
from .t_ax import TAx
from modusa.tools.math_ops import MathOps
from typing import Self, Any
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

class Audio(TDS):
	"""
	Represents a 1D audio signal within modusa framework.

	Note
	----
	- Use :class:`~modusa.generators.audio.AudioGen` to instantiate this class.
	- Audio must be mono (1D numpy array).

	Parameters
	----------
	y: Data
		- Data object holding the main audio data.
	t: TAx
		- Time axis for the audio.
	title: str
		- Title for the signal.
		- Default: None => ''
		- e.g. "MySignal"
		- This is used as the title while plotting.
	"""

	#--------Meta Information----------
	_name = "Audio Signal"
	_nickname = "Audio"
	_description = ""
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-04"
	#----------------------------------
	
	@validate_args_type()
	def __init__(self, y, t, title = None):

		super().__init__(y=y, t=t, title=title) # Instantiating `TimeDomainSignal` class
	
	#----------------------------------
	# Utility Tools
	#----------------------------------
			
	def play(self, regions = None, title = None):
		"""
		Play the audio signal inside a Jupyter Notebook.
	
		.. code-block:: python
	
			import modusa as ms
			audio = ms.audio.from_youtube("https://www.youtube.com/watch?v=lIpw9-Y_N0g")
			audio.play(regions=[(10, 30, "1")])
	
		Parameters
		----------
		regions : list[tuple[float, float, str], ...] | None
			- [(start_time, end_time, 'tag'), ...] pairs in seconds specifying the regions to play.
			- e.g. [(1, 10, "Segement 1"), (20, 25, "Segment 2")]
			- Default to None for which the entire signal is played.
		title : str | None
			- Title for the player interface. 
			- Defaults to None, which means that the signal’s internal title is used.
	
		Returns
		-------
		IPython.display.Audio
			An interactive audio player widget for Jupyter environments.

		See Also
		--------
		:class:`~modusa.tools.audio_player.AudioPlayer`
		"""
		
		from modusa.tools.audio_player import AudioPlayer

		title = title if title is not None else self.title

		audio_player = AudioPlayer.play(y=self.y.values, sr=self.t.sr, t0=self.t.t0, regions=regions, title=title)
		
		return audio_player