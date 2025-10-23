#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 22/10/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import numpy as np

def synth_f0(f0, f0t, sr, nharm=0):
	"""
	Synthesize f0 contour so that you can
	hear it back.

	Parameters
	----------
	f0: ndarray
		- Fundamental frequency (f0) contour in Hz.
	f0t: ndarray
		- Timestamps in seconds
	sr: int
		- Sampling rate in Hz for the synthesized audio.
	nharm: int
		- Number of harmonics
		- Default: 0 => Only fundamental frequency (No harmonics)

	Returns
	-------
	ndarray
		- Syntesized audio.
	sr
		- Sampling rate of the synthesized audio
	"""
	
	# Create new time axis
	t = np.arange(0, f0t[-1], 1 / sr)
	
	# Interpolate the f0 to match the sampling time points
	f0_interp = np.interp(t, f0t, f0)
	
	# Compute phase by integrating frequency over time
	phase = 2 * np.pi * np.cumsum(f0_interp) / sr
	
	# Start with fundamental
	y = np.sin(phase)
	
	# Add harmonics if requested
	for n in range(2, nharm + 2):  # from 2nd to (nharm+1)th harmonic
		y += np.sin(n * phase) / n**2  # dividing by n to reduce harmonic amplitude
	
	# Normalize output to avoid clipping
	y /= np.max(np.abs(y))
	
	return y, sr

def synth_clicks(event_times, sr, freq=500, nharm=4, click_duration_ms=5):
	"""
	Generate a train of short sine wave clicks with harmonics at specified event times.

	Parameters
	----------
	event_times : array-like
		- Times of events in seconds where clicks should be placed.
	sr : int
		- Sampling rate in Hz.
	freq : float, optional
		- Fundamental frequency of the sine click in Hz. Default is 500 Hz.
	nharm : int | None
		- Number of harmonics to include (including fundamental). Default is 4.
	click_duration_ms : float | None
		- Duration of each click in milliseconds. Default is 5 ms.
	
	Returns
	-------
	np.ndarray
		- Audio signal with sine wave clicks (with harmonics) at event times.
	int
		- Sampling rate of the generated click audio.
	"""
	
	n_samples = int(np.ceil(sr * event_times[-1]))
	y = np.zeros(n_samples, dtype=np.float32)
	
	# Single click length
	click_len = int(sr * click_duration_ms / 1000)
	if click_len < 1:
		click_len = 1
		
	t = np.arange(click_len) / sr
	window = np.hanning(click_len)
	
	# Generate harmonic sine click
	sine_click = np.zeros(click_len)
	for n in range(1, nharm+2):
		sine_click += (1 / n**2) * np.sin(2 * np.pi * freq * n * t)
		
	# Apply window
	sine_click = sine_click * window**2
	
	for event_time in event_times:
		start_sample = int(event_time * sr)
		end_sample = start_sample + click_len
		if end_sample > n_samples:
			end_sample = n_samples
		y[start_sample:end_sample] += sine_click[:end_sample - start_sample]
		
	# Normalize to avoid clipping if clicks overlap
	y /= np.max(np.abs(y))
	
	return y, sr

