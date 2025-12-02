#---------------------------------
# Author: Ankit Anand
# Date: 19-11-2025
# Email: ankit0.anand0@gmail.com
#---------------------------------

import numpy as np

class Audio:
  """
  Audio model to handle manipulating,
  analyzing and exporting audio files of various
  formats.

  Since I plan to support multi-channel processing,
  the audio data will be stored as ndarray with
  ndim = 2, (#channels, #samples).
  
  For mono: (1, #samples)
  For stereo: (2, #samples)
  """
  def __init__(self, data: np.ndarray, sr: int, title: str|None = None):
    #============================================
    # I should list all the internal state 
    # parameters so that the maintainers knows 
    # what are they.
    # _data: holds the actual audio array
    # _sr: sampling rate of the loaded audio
    # _ch: number of channels
    # title: title of the audio object, can be used
    # for plotting
    #============================================
    if not isinstance(data, np.ndarray) or not isinstance(sr, int | float):
      raise ValueError(f"'y' and 'sr' must be of type np.ndarray and int respectively, got {type(data), type(sr)} instead")
    if data.ndim != 2:
      raise ValueError(f"'y' must be of ndim=2, got {data.ndim} instead. For mono, please wrap it as (#channels, #samples) format.")
    
    self._data: np.ndarray = data
    self._sr: int = sr
    self._ch: int = data.shape[0]
    self.title: str|None = title # This is set to audio filename ow user can set it later.

  @property
  def data(self):
    return self._data

  @property
  def sr(self):
    return self._sr
  
  @property
  def size(self):
    return self.data.size
  
  @property
  def ch(self):
    """Number of channels."""
    return self._ch
  
  @property
  def shape(self):
    return self.data.shape
  
  def __repr__(self) -> str:
    ch_str = {1: "mono", 2: "stereo"}
    return f"Audio(y={self.data}, shape={self.shape} sr={self.sr}, ch={ch_str[self.ch]})"
  
  def __array__(self, copy=True):
    """This makes audio object compatible with numpy arrays."""
    return self.data
