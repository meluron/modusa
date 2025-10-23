#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 23/10/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import numpy as np

def stft(y, sr, winlen=None, hoplen=None, gamma=None):
	"""
	Compute spectrogram with just numpy.

	Parameters
	----------
	y: ndarray
		- Audio signal.
	sr: int
		- Sampling rate of the audio signal.
	winlen: int
		- Window length in samples.
		- Default: None => set at 0.064 sec
	hoplen: int
		- Hop length in samples.
		- Default: None => set at one-forth of winlen
	gamma: int | None
		- Log compression factor.
		- Add contrast to the plot.

	Returns
	-------
	ndarray:
		- Spectrogram matrix, complex is gamma is None else real
	ndarray:
		- Frequency bins in Hz.
	ndarray:
		- Timeframes in sec.
	"""
	
	if winlen is None:
		winlen = 2 ** int(np.log2(0.064 * sr))
	if hoplen is None:
		hoplen = int(winlen * 0.25)
		
	# Estimating the shape of the S matrix
	M = int(np.ceil(winlen / 2))
	N = int(np.ceil((y.size - winlen) / hoplen))
	
	# Initialize the S matrix
	S = np.empty((M, N), dtype=np.complex64) # M X N => freq bin X time frame
	
	# We will need a hann window
	hann = np.hanning(winlen)
	
	# Get the frames
	frames = np.lib.stride_tricks.sliding_window_view(y, window_shape=winlen)[::hoplen] # frame X chunk
	
	# Apply window to the frame
	frames_windowed = frames * hann # frame X chunk
	
	# Compute fft for each frame
	S = np.fft.rfft(frames_windowed, n=winlen, axis=1).T  # transpose to match shape (freq_bins, frame)
	
	# Magnitude spectrogram
	Sf = np.fft.rfftfreq(winlen, d=1/sr) # Frequency bins (Hz)
	St = np.arange(N) * hoplen / sr # Time bins (sec)
	
	if gamma is not None:
		S = np.log1p(gamma * np.abs(S))
		
	return S, Sf, St