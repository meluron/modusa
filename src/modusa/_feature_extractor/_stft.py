#---------------------------------
# Author: Ankit Anand
# Date: 23-11-2025
# Email: ankit0.anand0@gmail.com
#---------------------------------

import numpy as np

class STFTExtractor:
  """
  A class to extract STFT of an audio signal.
  """ 
  def extract(y, sr, winlen, hoplen, gamma):
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

    Returns
    -------
    ndarray:
      Spectrogram matrix, complex is gamma is None else real
    ndarray:
      Frequency bins in Hz.
    ndarray:
      Timeframes in sec.
    """
    
    #============================================
    # Setup the STFT params if not explicitely 
    # passed by the user.
    # window length = 0.064 sec 
    # hop length = 25 % of the window length
    #============================================
    if winlen is None:
      winlen = 2 ** int(np.log2(0.064 * sr))
    if hoplen is None:
      hoplen = int(winlen * 0.25)
        
    #============================================
    # I should initialize an empty array to hold 
    # the spectrogram matrix.
    #============================================

    #-------- Estimate the expected shape of the spectrogram matrix ---------
    M = int(np.ceil(winlen / 2))
    N = int(np.ceil((y.size - winlen) / hoplen))

    #-------- Instantiate the matrix (M, N) => (#freq bins, #time frames) ---------
    S = np.empty((M, N), dtype=np.complex64)
    
    #============================================
    # I should apply window on the input
    # signal using hanning window which is usually 
    # the default choice.
    #============================================
    
    hann = np.hanning(winlen)

    #-------- I am using sliding_window_view for efficiency as it creates only a view and not a new numpy array. ---------
    frames = np.lib.stride_tricks.sliding_window_view(y, window_shape=winlen)[::hoplen] # frame X chunk
  
    frames_windowed = frames * hann # frame X chunk
    
    #============================================
    # I want to compute the fft on the framed 
    # windowed signal to get the spectrogram.
    #============================================

    #-------- rfft is used instead of fft because the signal is assumed to be real-valued like audio signal. ---------
    #-------- Transposition is done to have the S matrix in used to format (#freq bins, #time frames). ---------
    S = np.fft.rfft(frames_windowed, n=winlen, axis=1).T 
    
    #-------- I then compute the corresponding freq bin -> freq (Hz) mapping, time frame -> time (sec) mapping. ---------
    Sf = np.fft.rfftfreq(winlen, d=1/sr) # Frequency bins (Hz)
    St = np.arange(N) * hoplen / sr # Time bins (sec)
    
    #============================================
    # I apply log-compression to enhance the
    # contrast of the spectrogram.
    #============================================
    if gamma is not None:
      S = np.log1p(gamma * np.abs(S))
        
    return S, Sf, St
