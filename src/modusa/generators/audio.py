#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import validate_args_type
from .base import ModusaGenerator
from modusa.models.t_ax import TAx
from modusa.models.audio import Audio
from modusa.models.data import Data
import numpy as np
from pathlib import Path

class AudioGen(ModusaGenerator):
	"""
	Provides user friendly APIs to generate instances of different 
	`AudioSignal` instances.
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
		y: np.ndarray,
		sr: float | int = 1.0,
		t0: float | int = 0.0,
		y_label: str = "Amplitude",
		t_label: str = "Time (sec)",
		title: str = "Audio Signal"
	) -> Audio:
		"""
		Create `AudioSignal` instance from basic data structures.

		.. code-block:: python

			import modusa as ms
			t = ms.tds.from_array([1, 2, 3])
			print(t)
			t.print_info()
		
		Parameters
		----------
		y: np.ndarray
			- Audio data array.
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
		Audio
			An instance of Audio.
		"""
		assert isinstance(y, np.ndarray)
		assert isinstance(sr, (int, float)) and isinstance(t0, (int, float))
		assert isinstance(y_label, str) and isinstance(t_label, str) and isinstance(title, str)
		
		assert y.ndim == 1
		
		sr = float(sr)
		t0 = float(t0)
		
		t = TAx(n_points=y.shape[0], sr=sr, t0=t0, label=t_label) # Creating a signal axis instance
		y = Data(values=y, label=y_label)
		
		return Audio(y=y, t=t, title=title)
	
	@classmethod
	def from_youtube(cls, url: str, sr: int | float = None):
		"""
		Loads audio from youtube at a given sr.
		The audio is deleted from the device
		after loading.
		
		.. code-block:: python
			
			import modusa as ms
			audio = ms.audio.from_youtube(
				url="https://www.youtube.com/watch?v=lIpw9-Y_N0g", 
				sr=None
			)

		PARAMETERS
		----------
		url: str
			Link to the YouTube video.
		sr: int
			Sampling rate to load the audio in.
		
		Returns
		-------
		Audio:
			An `Audio` instance with loaded audio content from YouTube.
		"""
		
		from modusa.tools.youtube_downloader import YoutubeDownloader
		from modusa import convert
		import soundfile as sf
		from scipy.signal import resample
		import tempfile
		
		# Download the audio in temp directory using tempfile module
		with tempfile.TemporaryDirectory() as tmpdir:
			audio_fp: Path = YoutubeDownloader.download(url=url, content_type="audio", output_dir=Path(tmpdir))
			
			# Convert the audio to ".wav" form for loading
			wav_audio_fp: Path = convert(inp_audio_fp=audio_fp, output_audio_fp=audio_fp.with_suffix(".wav"))
			
			# Load the audio in memory
			audio_data, audio_sr = sf.read(wav_audio_fp)
			
			# Convert to mono if it's multi-channel
			if audio_data.ndim > 1:
				audio_data = audio_data.mean(axis=1)
				
			# Resample if needed
			if sr is not None:
				if audio_sr != sr:
					n_samples = int(len(audio_data) * sr / audio_sr)
					audio_data = resample(audio_data, n_samples)
					audio_sr = sr
					
		audio = cls.from_array(y=audio_data, sr=audio_sr, title=audio_fp.stem)
		
		return audio
	
	@classmethod
	def from_filepath(cls, fp: str | Path, sr: int | float = None):
		"""
		Loads audio from filepath at a given sr.
		
		.. code-block:: python
			
			import modusa as ms
			audio = ms.audio.from_filepath(
				fp="path/to/audio.wav",
				sr=None
			)

		PARAMETERS
		----------
		fp: str | Path
			Audio file path.
		sr: int
			Sampling rate to load the audio in.
		
		Returns
		-------
		Audio:
			An `Audio` instance with loaded audio content.
		"""
		import soundfile as sf
		from scipy.signal import resample
		from pathlib import Path
		
		fp = Path(fp)
		# Load the audio in memory
		audio_data, audio_sr = sf.read(fp)
		
		# Convert to mono if it's multi-channel
		if audio_data.ndim > 1:
			audio_data = audio_data.mean(axis=1)
			
		# Resample if needed
		if sr is not None:
			if audio_sr != sr:
				n_samples = int(len(audio_data) * sr / audio_sr)
				audio_data = resample(audio_data, n_samples)
				audio_sr = sr
				
		audio = cls.from_array(y=audio_data, sr=audio_sr, title=fp.stem)
		
		return audio
	