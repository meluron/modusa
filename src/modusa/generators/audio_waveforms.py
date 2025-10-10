#!/usr/bin/env python3


from modusa import excp
from modusa.decorators import validate_args_type
from modusa.generators.base import ModusaGenerator
from modusa.models.audio_signal import AudioSignal
import numpy as np

class AudioWaveformGenerator(ModusaGenerator):
	"""
	Generates different kinds of audio waveforms particulary helpful
	in teaching signal processing concepts and testing out newly
	created tools.
	"""
	
	#--------Meta Information----------
	_name = "Audio Waveform Generator"
	_description = "Generates different kind of audio waveforms."
	_author_name = "Ankit Anand"
	_author_email = "ankit0.anand0@gmail.com"
	_created_at = "2025-07-07"
	#----------------------------------
	
	@staticmethod
	def generate_example() -> "AudioSignal":
		"""
		Generates a simple sine wave audio signal as an example.
	
		Returns
		-------
		AudioSignal
			A 600 Hz sine wave lasting 2 seconds, sampled at 10,000 Hz.
		"""
		
		sr = 10000 # Hz
		duration = 2 # sec
		freq = 600 # Hz
		
		t = np.arange(0, duration, 1 / sr)
		y = np.sin(2 * np.pi * freq * t)
		
		signal = AudioSignal(y=y, sr=sr, title="Example")  # assuming AudioSignal accepts y and t
		
		return signal
	
	
	@staticmethod
	def generate_random(duration: float = 1.0, sr: int = 10000) -> "AudioSignal":
		"""
		Generates a random audio signal of given duration and sample rate.
	
		Parameters
		----------
		duration : float, optional
			Duration of the signal in seconds (default is 1.0).
		sr : int, optional
			Sampling rate in Hz (default is 10,000).
	
		Returns
		-------
		AudioSignal
			A randomly generated signal of the specified duration and sample rate.
		"""
		num_samples = int(duration * sr)
		t = np.linspace(0, duration, num=num_samples, endpoint=False)
		y = np.random.uniform(low=-1.0, high=1.0, size=num_samples)  # use uniform [-1, 1] for audio-like signal
		
		signal = AudioSignal(y=y, t=t, title="Random")
		
		return signal
	
	@staticmethod
	@validate_args_type()
	def generate_sinusoid(
		A: float | int = 1.0,
		f: float | int = 10.0,
		phi: float | int = 0.0,
		duration: float | int = 1.0,
		sr: int = 1000,
	) -> "AudioSignal":
		"""
		Generates a sinusoid audio signal with specified
		amplitude, frequency, phase, duration, and sample rate.
	
		Parameters
		----------
		A : float
			Amplitude of the sinusoid (default: 1.0)
		f : float
			Frequency in Hz (default: 10.0)
		phi : float
			Phase in radians (default: 0.0)
		duration : float
			Duration of the signal in seconds (default: 1.0)
		sr : int
			Sampling rate in Hz (default: 1000)
	
		Returns
		-------
		AudioSignal
			A sinusoidal signal with the given parameters.
		"""
		A, f, phi, duration, sr = float(A), float(f), float(phi), float(duration), int(sr)
		
		t = np.arange(0, duration, 1 / sr)
		y = A * np.sin(2 * np.pi * f * t + phi)
		
		signal = AudioSignal(y=y, sr=sr, title=f"Sinusoid ({f} Hz)")
		
		return signal
	
	@staticmethod
	@validate_args_type()
	def generate_square(
		A: float | int = 1.0,
		f: float | int = 10.0,
		phi: float | int = 0.0,
		duration: float | int = 1.0,
		sr: int = 1000,
	) -> "AudioSignal":
		"""
		Generates a square wave audio signal with specified
		amplitude, frequency, phase, duration, and sample rate.
	
		Parameters
		----------
		A : float
			Amplitude of the square wave (default: 1.0)
		f : float
			Frequency in Hz (default: 10.0)
		phi : float
			Phase in radians (default: 0.0)
		duration : float
			Duration of the signal in seconds (default: 1.0)
		sr : int
			Sampling rate in Hz (default: 1000)
	
		Returns
		-------
		AudioSignal
			A square wave signal of the specified parameters.
		"""
		A, f, phi, duration, sr = float(A), float(f), float(phi), float(duration), int(sr)
		t = np.arange(0, duration, 1 / sr)
		
		y = A * np.sign(np.sin(2 * np.pi * f * t + phi))
		
		signal = AudioSignal(y=y, sr=sr, title=f"Square ({f} Hz)")
		
		return signal
	
	
	@staticmethod
	@validate_args_type()
	def generate_sawtooth(
		A: float | int = 1.0,
		f: float | int = 10.0,
		phi: float | int = 0.0,
		duration: float | int = 1.0,
		sr: int = 1000,
	) -> "AudioSignal":
		"""
		Generates a sawtooth wave AudioSignal with specified amplitude, frequency, phase, duration, and sample rate.
	
		Parameters
		----------
		A : float
			Amplitude of the sawtooth wave (default: 1.0)
		f : float
			Frequency in Hz (default: 10.0)
		phi : float
			Phase in radians (default: 0.0)
		duration : float
			Duration of the signal in seconds (default: 1.0)
		sr : int
			Sampling rate in Hz (default: 1000)
	
		Returns
		-------
		AudioSignal
			A sawtooth wave signal of the specified parameters.
		"""
		A, f, phi, duration, sr = float(A), float(f), float(phi), float(duration), int(sr)
		t = np.arange(0, duration, 1 / sr)
		
		# Convert phase from radians to fractional cycle offset
		phase_offset = phi / (2 * np.pi)
		y = A * (2 * ((f * t + phase_offset) % 1) - 1)
		
		signal = AudioSignal(y=y, sr=sr, title=f"Sawtooth ({f} Hz)")
		return signal
	
	
	@staticmethod
	@validate_args_type()
	def generate_triangle(
		A: float | int = 1.0,
		f: float | int = 10.0,
		phi: float | int = 0.0,
		duration: float | int = 1.0,
		sr: int = 1000,
	) -> "AudioSignal":
		"""
		Generates a triangle wave AudioSignal with specified
		amplitude, frequency, phase, duration, and sample rate.
	
		Parameters
		----------
		A : float
			Amplitude of the triangle wave (default: 1.0)
		f : float
			Frequency in Hz (default: 10.0)
		phi : float
			Phase in radians (default: 0.0)
		duration : float
			Duration of the signal in seconds (default: 1.0)
		sr : int
			Sampling rate in Hz (default: 1000)
	
		Returns
		-------
		AudioSignal
			A triangle wave signal of the specified parameters.
		"""
		A, f, phi, duration, sr = float(A), float(f), float(phi), float(duration), int(sr)
		t = np.arange(0, duration, 1 / sr)
		phase_offset = phi / (2 * np.pi)  # Convert radians to cycle offset
		
		# Triangle wave formula: 2 * abs(2 * frac(x) - 1) - 1 scaled to amplitude
		y = A * (2 * np.abs(2 * ((f * t + phase_offset) % 1) - 1) - 1)
		
		signal = AudioSignal(y=y, sr=sr, title=f"Triangle ({f} Hz)")
		
		return signal
	