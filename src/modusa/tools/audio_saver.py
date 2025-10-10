#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 13/09/25
# Email: ankit0.anand0@gmail.com
#---------------------------------


def save(y, sr, out_path):
	"""
	Saves an array as an audio file.
	
	Parameters
	----------
	y: ndarray
		- Audio signal array.
	sr: number [> 0]
		- Sampling rate of the audio signal.
	out_path: str
		- Output path of the audio file.
	
	Returns
	-------
	None
	"""
	
	import soundfile as sf
	
	sf.write(file=out_path, data=y, samplerate=sr)
