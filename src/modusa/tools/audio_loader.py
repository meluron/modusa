#!/usr/bin/env python3


import subprocess
import numpy as np
import imageio_ffmpeg as ffmpeg
from pathlib import Path
import re

def _get_audio_info_ffmpeg(path: Path):
	"""
	To get the original sampling rate and number of
	channels of a given audio file by parsing the
	metadata. (No extra tool required).

	Parameters
	----------
	audiofp: PathLike
		- Audio filepath
	
	Returns
	-------
	int
		- Original sampling rate (hz)
	int
		- Number of channels
	"""
	ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
	cmd = [ffmpeg_exe, "-i", str(path)]
	proc = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
	text = proc.stderr
	
	# Example parse: "Stream #0:0: Audio: mp3, 44100 Hz, stereo, ..."
	m = re.search(r'Audio:.*?(\d+)\s*Hz.*?(mono|stereo)', text)
	if not m:
		raise RuntimeError("Could not parse audio info")
	sr = int(m.group(1))
	channels = 1 if m.group(2) == "mono" else 2
	return sr, channels

def _load_audio_from_youtube(url: str):
	"""
	Download audio from a YouTube URL, convert it to WAV, and return the path.

	Parameters
	----------
	url : str
		YouTube video URL.

	Returns
	-------
	Path
		Path to the converted WAV file (you can delete it later).
	"""
	from modusa.tools.youtube_downloader import download
	from modusa.tools.audio_converter import convert
	import tempfile
	
	# Temporary directory to hold files (auto-created, not auto-deleted)
	tmpdir = Path(tempfile.mkdtemp())
	
	# Download YouTube audio (e.g. .m4a or .webm)
	audio_fp: Path = download(url=url, content_type="audio", output_dir=tmpdir)
	
	# Convert downloaded file to .wav
	wav_audio_fp: Path = convert(inp_audio_fp=audio_fp, output_audio_fp=audio_fp.with_suffix(".wav"))
	
	# Return path to the WAV file
	return wav_audio_fp

#---------------------
# Main Function
#---------------------
def load(path, sr=None, trim=None, ch=None):
	"""
	Lightweight audio loader using imageio-ffmpeg.

	Parameters
	----------
	path: PathLike/str/URL
		- Path to the audio file / YouTube video
	sr: int
		- Sampling rate to load the audio in.
		- Default: None => Use the original sampling rate
	trim: tuple[number, number]
		- (start, end) in seconds to trim the audio clip.
		- Default: None => No trimming
	ch: int
		- 1 for mono and 2 for stereo
		- Default: None => Use the original number of channels.

	Returns
	-------
	np.ndarray
		- Audio signal Float32 waveform in [-1, 1].
	int:
		Sampling rate.
	str:
		File name stem.
	"""
	path = Path(path)
	
	# If the path is a YouTube URL, turn on the yt flag
	yt = False # By default, set to false
	if ".youtube" in str(path):
		yt = True
	
	# For local files, check if the audio exists
	elif not path.exists():
		raise FileExistsError(f"{path} does not exist")
	
	ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
	
	if yt:
		try:
			path: Path = _load_audio_from_youtube(url=str(path))
		except Exception as e:
			raise ConnectionRefusedError("unable to download from YouTube")
	
	# Find the real sample rate from the file
	if sr is None:
		sr, _ = _get_audio_info_ffmpeg(path)
		if not (sr > 100 and sr < 80000):
			raise Exception(f"Error reading the metadata for original sampling rate {sr}, please set `sr` explicitly")
	
	# Find the real number of channels from the file
	if ch is None:
		_, ch = _get_audio_info_ffmpeg(path)
		
		if ch not in [1, 2]:
			raise Exception(f"Error reading the metadata for number of channels {ch}, please set `ch` explicitly")
		
	cmd = [ffmpeg_exe]
	
	# Optional trimming
	if trim is not None:
		start, end = trim
		duration = end - start
		cmd += ["-ss", str(start), "-t", str(duration)]
		
	cmd += ["-i", str(path), "-f", "s16le", "-acodec", "pcm_s16le"]
	cmd += ["-ar", str(sr)]
	cmd += ["-ac", str(ch)]
		
	cmd += ["-"]
	
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
	raw = proc.stdout.read()
	proc.wait()
	
	audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
	
	# Stereo reshaping if forced
	if ch == 2:
		audio = audio.reshape(-1, 2).T
		
	# Delete the file if downloaded from youtube
	if yt:
		path.unlink(missing_ok=True)
		path.parent.rmdir()
		
	return audio, sr, path.stem
