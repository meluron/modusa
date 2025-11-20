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
  
  def __init__(self, audiofp: str|Path|None = None, y: np.ndarray|None = None, sr: int|None = None, ch: int|None = None):
    
    # == List all the internal state parameters so that the dev knows what are they.
    self._y: np.ndarray | None = None
    self._sr: int | None = None
    self._ch: int | None = None
    self.title: str | None = None

    # == If the audio filepath is provided, Load it using FFMPEG and update the internal state (in the function)
    if audiofp is not None:
      y, sr, ch, title = Audio._load_from_file(audiofp=audiofp, sr=sr, ch=ch)
      # ==== Update the internal state
      self._y, self._sr, self._ch, self.title = y, sr, ch, title

    # == If the audio file path is not provided, we set the internal state as per the arguments value
    else:
      # ==== Raise error if y and sr are not provided
      if not isinstance(y, np.ndarray) or not isinstance(sr, int | float):
        raise ValueError(f"'y' and 'sr' must be of type np.ndarray and int respectively, got {type(y), type(sr)} instead")
      if y.ndim not in [1, 2]:
        raise ValueError("'y' must be either 1 or 2 channel, got {y.ndim} instead")
      # ==== Set the internal states
      self._y, self._sr, self._ch = y, sr, y.ndim

  @property
  def y(self):
    return self._y

  @property
  def sr(self):
    return self._sr
  
  @property
  def size(self):
    return self.y.size
  
  @property
  def ch(self):
    return self._ch
  
  @property
  def shape(self):
    return self.y.shape
  
  def __repr__(self) -> str:
    ch_str = {1: "mono", 2: "stereo"}
    return f"Audio(y={self.y}, shape={self.shape} sr={self.sr}, ch={ch_str[self.ch]})"
  
  def __array__(self, copy=True):
    return self.y

  @staticmethod
  def _load_from_file(audiofp: str|Path, sr: int|None, ch: int|None):
    """
    Lightweight audio loader using imageio-ffmpeg.

    Parameters
    ----------
    audiofp: PathLike | str
      Path to the audio file
    sr: int
      Sampling rate to load the audio in.
      Default: None => Use the original sampling rate
    trim: tuple[number, number]
      (start, end) in seconds to trim the audio clip.
      Default: None => No trimming
    ch: int
      1 for mono and 2 for stereo
      Default: None => Use the original number of channels.

    Returns
    -------
    np.ndarray
      Audio signal Float32 waveform in [-1, 1].
    int:
      Sampling rate.
    int:
      Number of channels
    str:
      File name stem.
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
    if ch == 2:
      audio = audio.reshape(-1, 2).T

    return audio, sr, ch, audiofp.stem
  

