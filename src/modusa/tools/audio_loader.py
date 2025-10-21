#!/usr/bin/env python3


import soundfile as sf
from scipy.signal import resample
import numpy as np
from pathlib import Path
import tempfile
from scipy.signal import resample
from .youtube_downloader import download
from .audio_converter import convert

def load(path, sr=None, trim=None, mono=True):
	"""
	Loads audio file from various sources.

	.. code-block:: python
		
		import modusa as ms
		audio_fp = ms.load(
			"https://www.youtube.com/watch?v=lIpw9-Y_N0g",
			sr = None, trim=(5, 10))

	Parameters
	----------
	path: str
		- Path to the audio file.
		- YouTube URL.
	sr: int | None
		- Sampling rate to load the audio in.
	trim: number | tuple[number, number] | None
		- Segment of the audio to load.
		- Example: 10 => First 10 seconds, (5, 10) => 5 to 10 seconds.
		- Default: None => Entire audio.
	mono: bool
		- If True, loads the signal in mono.

	Return
	------
	np.ndarray
		- Audio signal.
	int
		- Sampling rate of the loaded audio signal.
	title
		- Title of the loaded audio.
		- Filename without extension or YouTube title.
	"""
	# Check if the path is YouTube
	if ".youtube." in str(path):
		# Download the audio in temp directory using tempfile module
		with tempfile.TemporaryDirectory() as tmpdir:
			# Download
			audio_fp: Path = download(url=path, content_type="audio", output_dir=Path(tmpdir))
			
			# Convert the audio to ".wav" form for loading
			wav_audio_fp: Path = convert(inp_audio_fp=audio_fp, output_audio_fp=audio_fp.with_suffix(".wav"))
			
			# Load the audio in memory
			audio_data, audio_sr = sf.read(wav_audio_fp)
			title = audio_fp.stem
	else:
		# Check if the file exists
		fp = Path(path)
		
		if not fp.exists():
			raise FileNotFoundError(f"{path} does not exist.")
			
		# Load the audio in memory
		audio_data, audio_sr = sf.read(fp)
		title = fp.stem
		
	# Convert to mono if requested and it's multi-channel
	if mono and audio_data.ndim > 1:
		audio_data = audio_data.mean(axis=1)
		
	# Resample if needed
	if sr is not None and audio_sr != sr:
		n_samples = int(len(audio_data) * sr / audio_sr)
		
		if audio_data.ndim == 1:
			# Mono
			audio_data = resample(audio_data, n_samples)
		else:
			# Stereo or multi-channel: resample each channel independently
			audio_data = np.stack([
				resample(audio_data[:, ch], n_samples)
				for ch in range(audio_data.shape[1])
			], axis=1)
			
		audio_sr = sr
		
	# Trim if requested
	if trim is not None:
		if isinstance(trim, (int, float)):
			trim = (0, trim)
		elif isinstance(trim, tuple) and len(trim) > 1:
			trim = (trim[0], trim[1])
		else:
			raise ValueError(f"Invalid trim type or length: {type(trim)}, len={len(trim)}")
			
		start = int(trim[0] * audio_sr)
		end = int(trim[1] * audio_sr)
		audio_data = audio_data[start:end]
		
	# Clip to avoid out-of-range playback issues
	if np.issubdtype(audio_data.dtype, np.floating):
		audio_data = np.clip(audio_data, -1.0, 1.0)
		
	return audio_data.T, audio_sr, title