import numpy as np

def stft(y, sr, winlen=None, hoplen=None, gamma=None):
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
    gamma: int | None
      Log compression factor.
      Add contrast to the plot.
      Default: None

    Returns
    -------
    ndarray:
      Spectrogram matrix, complex is gamma is None else real
    ndarray:
      Frequency bins in Hz.
    ndarray:
      Timeframes in sec.
    """
    
    # Parameter Setup
    if winlen is None:
        winlen = 2 ** int(np.log2(0.064 * sr))
    if hoplen is None:
        hoplen = int(winlen * 0.25)

    # Padding (Centering the windows)
    # Pad with zeros so the first frame is centered at t=0
    y_padded = np.pad(y, pad_width=winlen // 2, mode='constant')

    # Create Frames
    # Use sliding_window_view to create the frames
    frames = np.lib.stride_tricks.sliding_window_view(y_padded, window_shape=winlen)[::hoplen]
    
    # Apply Window
    hann = np.hanning(winlen)
    frames_windowed = frames * hann
    
    # Compute RFFT
    # We don't need to pre-allocate S; rfft creates it efficiently
    # Result shape: (number_of_frames, (winlen // 2) + 1)
    S = np.fft.rfft(frames_windowed, n=winlen, axis=-1).T 
    
    # Generate Mappings
    # Sf: frequency of each row in Hz
    # St: time of each column in seconds
    Sf = np.fft.rfftfreq(winlen, d=1/sr)
    num_frames = S.shape[1]
    St = np.arange(num_frames) * hoplen / sr
    
    # Log Compression
    if gamma is not None:
        S = np.log1p(gamma * np.abs(S))
        
    return S, Sf, St
