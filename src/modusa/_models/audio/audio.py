#---------------------------------
# Author: Ankit Anand
# Date: 19-11-2025
# Email: ankit0.anand0@gmail.com
#---------------------------------

import subprocess
import numpy as np
from pathlib import Path
import imageio_ffmpeg as ffmpeg
from .utils_loader import parse_sr_and_nchannels

class Audio:
  """
  Audio model to handle loading, manipulating,
  analyzing and exporting audio files of various
  formats.

  Since I plan to support multi-channel processing,
  the audio data will be stored as ndarray with
  ndim = 2, (#channels, #samples).
  
  For mono: (1, #samples)
  For stereo: (2, #samples)

  Parameters
  ----------
  audiofp: str|Path|None, default=None
    Local filepath of the audio file to be loaded.
  data: np.ndarray|None, default=None
    Incase you have already loaded the audio signal using some other libraries
    pass it here to create Audio object.
  sr: int|None, default=None
    The behavior of this parameter depends on whether you are loading audio using
    `audiofp` or `data` parameter.
    If you are using `audiofp`, then use this to load the audio in any desired sampling
    rate, the audio will be resampled using ffmpeg. If set to None, I look into the header
    and extracts the original sampling rate.
    If you are using `data`, then you are expected to know the sampling rate in which you
    already loaded your audio. You are required to pass that info correctly.
  ch: int|None, default=None, options=[1, 2, None]
    The behavior of this parameter depends on whether you are loading audio using
    `audiofp` or `data` parameter.
    If you are using `audio_fp`, then use this to load the audio signal into either 
    mono (ch=1) or stereo (ch=2). If set to None, I look into the header and extracts 
    the original number of channels.
    If you are using `data`, then this will be set automatically based on the 
    ndim of the `data` array no need to pass anything. You need to make sure 
    that you are passing the data in the expected format.
    For mono: (#samples) => ndim = 1
    For stereo: (#channels, #samples) => ndim = 2 and shape[0] == 2
  """
  def __init__(self, audiofp: str|Path|None = None, data: np.ndarray|None = None, sr: int|None = None, ch: int|None = None):
    
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
    self._data: np.ndarray | None = None
    self._sr: int | None = None
    self._ch: int | None = None
    self.title: str | None = None # This is set to audio filename ow user can set it later.

    #============================================
    # If the audio filepath is provided, 
    # I should load it using FFMPEG and update 
    # the internal state.
    #============================================
    if audiofp is not None:
      #-------- Convert the audiofp to Path object ---------
      audiofp = Path(audiofp)
      data, sr, ch, title = Audio._load_from_file(audiofp=audiofp, sr=sr, ch=ch)
      self._data, self._sr, self._ch, self.title = data, sr, ch, title

    #============================================
    # If the audio file path is not provided, 
    # I should set the internal state as per the 
    # arguments passed by the user.
    #============================================
    else:
      #-------- Raise error if y and sr are not provided ---------
      if not isinstance(data, np.ndarray) or not isinstance(sr, int | float):
        raise ValueError(f"'y' and 'sr' must be of type np.ndarray and int respectively, got {type(data), type(sr)} instead")
      if data.ndim != 2:
        raise ValueError(f"'y' must be of ndim=2, got {data.ndim} instead. For mono, please wrap it as (#channels, #samples) format.")
      #-------- Set the interal states ---------
      self._data, self._sr, self._ch = data, sr, data.ndim

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
  
  #============================================
  # The function should load audio from filepath
  #============================================
  @staticmethod
  def _load_from_file(audiofp:Path, sr: int|None, ch: int|None):
    """
    Lightweight audio loader using imageio-ffmpeg.

    Parameters
    ----------
    audiofp: Path
      Path to the audio file
    sr: int|None
      Sampling rate to load the audio in.
      Pass None to load in original sampling rate.
    ch: int|None
      1 for mono and 2 for stereo
      Pass None to load in original number of channels.

    Returns
    -------
    np.ndarray
      Audio signal Float32 waveform in [-1, 1].
    int:
      Sampling rate.
    int:
      Number of channels
    str:
      File name stem acting as the title of the audio object.
    """

    # == Raise an error if the audio file does not exist
    audiofp = Path(audiofp)
    if not audiofp.exists(): raise FileExistsError(f"{audiofp} does not exist")
    
    # == Parse the sr and nchannels info from the header and set sr, ch to the default
    default_sr, default_nchannels = parse_sr_and_nchannels(audiofp) # int, int
    # ==== Use the parsed sr and nchannels if not explicitely passed by the user
    if sr is None: sr = default_sr
    if ch is None: ch = default_nchannels

    # ==== Check if the ch is valid
    if ch not in [1, 2]:
      raise RuntimeError(f"'ch' must be either 1 or 2, got {ch} instead")
    
    # == Get the FFMPEG executable and run it with the correct configuration to get the audio array
    ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
    
    # ==== Setting up the configuration for FFMPEG
    cmd = [ffmpeg_exe]
    cmd += ["-i", str(audiofp), "-f", "s16le", "-acodec", "pcm_s16le"]
    cmd += ["-ar", str(sr)]
    cmd += ["-ac", str(ch)]
    cmd += ["-"]
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw = proc.stdout.read()
    proc.wait()
    
    # ==== Get the data as an array
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    
    # == Stereo reshaping if forced
    if ch == 1:
      audio = np.array([audio]) #  This is done to follow (#channels, #samples)
    if ch == 2:
      audio = audio.reshape(-1, 2).T

    return audio, sr, ch, audiofp.stem
