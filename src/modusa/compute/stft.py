import numpy as np

def stft(y, sr, winlen=None, hoplen=None):
    """
    Compute spectrogram using only numpy.

    Parameters
    ----------
    y: ndarray
      Audio signal.
    sr: int
      Sampling rate of the audio signal.
    winlen: int
      Window length in samples.
      Default: None => set at 0.064 sec
    hoplen: int
      Hop length in samples.
      Default: None => set at one-forth of winlen

    Returns
    -------
    ndarray:
      Spectrogram matrix
    ndarray:
      Frequency bins in Hz.
    ndarray:
      Timeframes in sec.
    """
    
    # Format input
    y = np.ascontiguousarray(y, dtype=np.float32)
    
    # Manual Periodic Hann Window (Matches scipy.signal.get_window('hann', fftbins=True))
    n = np.arange(winlen)
    window = (0.5 - 0.5 * np.cos(2.0 * np.pi * n / winlen)).astype(np.float32)
    
    # Padding (Reflect) - Centers the window at y[0]
    pad_width = winlen // 2
    y_padded = np.pad(y, pad_width=pad_width, mode='constant')
    
    # Efficient Framing
    all_frames = np.lib.stride_tricks.sliding_window_view(y_padded, window_shape=winlen)[::hoplen]
    
    # Boundary Calculation (Librosa standard)
    n_frames = 1 + (len(y_padded) - winlen) // hoplen
    frames = all_frames[:n_frames]
    
    # Windowing and FFT
    # Result is transposed to (Frequency, Time)
    S = np.fft.rfft(frames * window, n=winlen, axis=-1).T

    # Axis Bins
    freqs = np.fft.rfftfreq(winlen, d=1/sr)
    times = np.arange(S.shape[1]) * (hoplen / sr)
    
    return S, freqs, times
