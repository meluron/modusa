#---------------------------------
# Author: Ankit Anand
# Date: 02-12-2025
# Email: ankit0.anand0@gmail.com
#---------------------------------

import subprocess
from pathlib import Path
import imageio_ffmpeg as ffmpeg
import re
import numpy as np

from .audio import Audio
    

def parse_sr_and_nchannels(audiofp):
  """
  Given the header text of audio, parse
  the audio sampling rate and number of
  channels.

  Parameters
  ----------
  header_txt: str
    Extracted header text of the audio.

  Returns
  -------
  int
    Sampling rate.
  int
    Number of channels (1 or 2)
  """

  # Get the ffmpeg executable
  ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
  
  # Get the header text content from the audio file
  cmd = [ffmpeg_exe, "-i", str(audiofp)]
  proc = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
  header = proc.stderr

  m = re.search(r'Audio:.*?(\d+)\s*Hz.*?(mono|stereo)', header) # "Stream #0:0: Audio: mp3, 44100 Hz, stereo, ..."
  if not m:
      raise RuntimeError("Could not parse audio info")
  sr = int(m.group(1))
  channels = 1 if m.group(2) == "mono" else 2
  
  return sr, channels

def load_audio(fp: str|Path, sr: int|None = None, ch: int|None = None) -> Audio:
    """
    Lightweight audio loader using imageio-ffmpeg.
    
    Parameters
    ----------
    fp: str | Path
      Path to the audio file.
    sr: int | None (default=None => Load in original sampling rate.)
      Sampling rate to load the audio in.
    ch: int | None (default=None => Load in original number of channels.)

    Returns
    -------
    Audio
      Audio object with the content being loaded.
    """

    #============================================
    # I should raise an error if the audio file 
    # does not exist
    #============================================
    if not fp.exists(): raise FileExistsError(f"{fp} does not exist")
    
    #============================================
    # I should parse the audio file header to get
    # the original sr, ch to load the audio into.
    #============================================
    
    #-------- Parse the sr and nchannels info from the header ---------
    default_sr, default_nchannels = parse_sr_and_nchannels(fp) # int, int

    #-------- Use the parsed sr and nchannels if not explicitely passed by the user ---------
    if sr is None: sr = default_sr
    if ch is None: ch = default_nchannels

    #--------  I should check if the ch is valid (1, 2) ---------
    if ch not in [1, 2]:
      raise RuntimeError(f"'ch' must be either 1 or 2, got {ch} instead")
    
    #============================================
    # I should load the audio array using FFMPEG 
    # executatable
    #============================================
  
    ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
    
    cmd = [ffmpeg_exe]
    cmd += ["-i", str(fp), "-f", "s16le", "-acodec", "pcm_s16le"]
    cmd += ["-ar", str(sr)]
    cmd += ["-ac", str(ch)]
    cmd += ["-"]
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw = proc.stdout.read()
    proc.wait()
    
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    
    #-------- Adjust the shape of the audio array to match the requirements of the Audio object ---------
    if ch == 1:
      audio = np.array([audio]) #  This is done to follow (#channels, #samples)
    if ch == 2:
      audio = audio.reshape(-1, 2).T

    return Audio(audio, sr, fp.stem)
