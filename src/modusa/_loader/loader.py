# ---------------------------------
# Author: Ankit Anand
# Date: 04-12-2025
# Email: ankit0.anand0@gmail.com
# ---------------------------------


import modusa as ms
from pathlib import Path
import re
import warnings
import numpy as np
import subprocess
import imageio_ffmpeg as ffmpeg

class Loader:
  """
  A class that provides APIs to instantiate 
  modusa model classes like `ms.audio`, 
  `ms.annotation`.
  """

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

      # 04-12-2025 [Ankit Anand]: Extract the header of the audio file using FFMPEG console output.
      ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
      cmd = [ffmpeg_exe, "-i", str(audiofp)]
      proc = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
      header = proc.stderr

      # 04-12-2025 [Ankit Anand]: Using regular expression to extract sr and channels from the header.
      # "Audio: pcm_s16le ([1][0][0][0] / 0x0001), 48000 Hz, mono, s16" for wav
      # "Audio: mp3, 44100 Hz, stereo, ..." for mp3

      m = re.search(r'Audio:.*?(\d+)\s*Hz.*?(mono|stereo)', header)
      if not m:
          raise RuntimeError("could not parse audio info from the header.\n{header}")
      
      sr = int(m.group(1))

      if m.group(2) == "mono": 
        channels = 1
      elif m.group(2) == "stereo": 
        channels = 2
      else: 
        raise RuntimeError("could not find the channel info in the header.\n{header}")
 
      if not (isinstance(sr, int) and isinstance(channels, int)):
        raise ValueError(f"Invalid `sr` or `channels` type. Expected int but got `sr` as {type(sr)}) `channels` as {type(channels)} instead.")
      
      return sr, channels
  
  def audio(fp: str|Path, sr: int|None = None, ch: int|None = None) -> ms.audio:
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
    ms.audio
      Audio object with the content being loaded.
    """

    fp: Path = Path(fp)
    if not fp.exists(): raise FileExistsError(f"{fp} does not exist")

    # 04-12-2025 [Ankit Anand]: Parse the sr and nchannels info from the header of the audio file and set the sr and ch to parsed values if not passed by user.
    default_sr, default_nchannels = Loader.parse_sr_and_nchannels(fp) # int, int
    if sr is None: sr = default_sr
    if ch is None: ch = default_nchannels
    if ch not in [1, 2]: raise RuntimeError(f"'ch' must be either 1 or 2, got {ch} instead")
    
    # ============================================
    # 04-12-2025 [Ankit Anand]
    # I should load the audio array using FFMPEG 
    # executatable
    # ============================================

    ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
    
    cmd = [ffmpeg_exe]
    cmd += ["-i", str(fp), "-f", "s16le", "-acodec", "pcm_s16le"] # -f: s16le => raw PCM audio, no headers, -acodec: pcm_s16le => encode as uncompressed standard quality 
    cmd += ["-ar", str(sr)] # Setting the sampling rate to load the audio in.
    cmd += ["-ac", str(ch)] # Setting the number of channels to load the audio in.
    cmd += ["-"] # This tells ffmpeg to output the raw data into stdout that can be used to get the data without saving it.
    
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw = proc.stdout.read()
    proc.wait()
    
    # 04-12-2025 [Ankit Anand]: Convert the raw data into numpy array (normalized to have range between -1.0 and 1.0).
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    
    # 04-12-2025 [Ankit Anand]: Make sure that audio is 2D array. (#channels, #samples)
    # For mono: (1, N) and for stereo: (2, N)
    if ch == 1: audio = np.array([audio])
    if ch == 2: audio = audio.reshape(-1, 2).T

    return ms.audio(audio, sr, fp.stem)

  def audacity_label(fp: Path|str):
    """
    Loads audacity label text file as ms.annotation object.
    
    Parameters
    ----------
    fp: Path|str
      Filepath of the audacity label file.

    Returns
    -------
    ms.annotation
      Loaded annotation object.
    """

    fp: Path = Path(fp)
    if not fp.exists(): raise FileExistsError(f"{fp} does not exist.")

    data: list = [] # To store [(start, end, label, confidence, group), ...]

    with open(str(fp), "r") as f:
      lines = f.read().splitlines() # ["start end label", ...]

    for line in lines:
      # -- Ankit Anand on 04-12-2025 --
      # 04-12-2025 [Ankit Anand]: Ignore empty lines before parsing.
      if not line.strip():
        continue

      start, end, label = line.split("\t")
      start, end = float(start), float(end)
      data.append((start, end, label, None, None)) # The last two entries (confidence, group) are set to None
    
    return ms.annotation(data)

  def ctm(fp: Path|str):
    """
    Loads ctm file as Annotation object.
    
    Parameters
    ----------
    fp: Path|str
      Filepath of the ctm file.

    Returns
    -------
    ms.annotation
      Loaded annotation object.
    """

    fp: Path = Path(fp)
    if not fp.exists(): raise FileExistsError(f"{fp} does not exist.")

    data: list = [] # To store [(start, end, label, confidence, group), ...]

    with open(str(fp), "r") as f:
      lines = f.read().splitlines()
    
    for line in lines:
      # 04-12-2025 [Ankit Anand]: Ignore empty lines before parsing.
      if not line.strip():
        continue
      
      parts = line.split() # [utterance_id, channel, start, duration, label, confidence(optional)]

      # 04-12-2025 [Ankit Anand]: Handle ctm files that do not have confidence score.
      if len(parts) == 5:
        segment_id, channel, start, dur, label = parts
        start, dur = float(start), float(dur)
        confidence = None

      # 04-12-2025 [Ankit Anand]: Handle ctm files that have confidence score.
      elif len(parts) == 6:
        segment_id, channel, start, dur, label, confidence = parts
        start, dur = float(start), float(dur)
        confidence = float(confidence)
      
      # 04-12-2025 [Ankit Anand]: Handle any anamolies in any of the lines of the ctm.
      else:
        warnings.warn(f"'{line}' is not a standard ctm line <utterance_id channel start dur label confidence[optional]>.")
        continue
        
      data.append((start, start + dur, label, confidence, None))

    return ms.annotation(data)

  def textgrid(fp: Path|str):
    """
    Loads textgrid file as ms.annotation object.
    
    Parameters
    ----------
    fp: Path|str
      Filepath of the textgrid file.

    Returns
    -------
    ms.annotation
      Loaded annotation object.
    """

    fp: Path = Path(fp)
    if not fp.exists(): raise FileExistsError(f"{fp} does not exist.")

    data: list = []  # To store [(start, end, label, confidence, group), ...]

    with open(str(fp), "r") as f:
      lines = [line.strip() for line in f]
    
    in_interval = False
    s = e = None
    label = ""
    
    for line in lines:
      # detect start of interval
      if line.startswith("intervals ["):
        in_interval = True
        s = e = None
        label = ""
        continue
      
      if in_interval:
        if line.startswith("xmin ="):
          s = float(line.split("=")[1].strip())
        elif line.startswith("xmax ="):
          e = float(line.split("=")[1].strip())
        elif line.startswith("text ="):
          label = line.split("=", 1)[1].strip().strip('"')
            
          # Finished reading an interval
          if label != "" and s is not None and e is not None:
            data.append((s, e, label, None, None))
          in_interval = False  # Ready for next interval
    
    return ms.annotation(data)
