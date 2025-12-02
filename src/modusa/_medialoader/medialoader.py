#---------------------------------
# Author: Ankit Anand
# Date: 02-12-2025
# Email: ankit0.anand0@gmail.com
#---------------------------------

import modusa as ms
from pathlib import Path
import re
import warnings
import numpy as np
import subprocess
import imageio_ffmpeg as ffmpeg


class MediaLoader:
  """"""

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

    #============================================
    # I should raise an error if the audio file 
    # does not exist
    #============================================
    fp: Path = Path(fp)
    if not fp.exists(): raise FileExistsError(f"{fp} does not exist")
    
    #============================================
    # I should parse the audio file header to get
    # the original sr, ch to load the audio into.
    #============================================
    
    #-------- Parse the sr and nchannels info from the header ---------
    default_sr, default_nchannels = MediaLoader.parse_sr_and_nchannels(fp) # int, int

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

    return ms.audio(audio, sr, fp.stem)    

  def audacity_label(fp: Path|str):
    """
    Loads audacity label text file as Annotation object.
    
    Parameters
    ----------
    fp: Path|str
      Filepath of the audacity label file.

    Returns
    -------
    Annotation
      Loaded annotation object.
    """
    #============================================
    # I should raise error if the file does not
    # exist.
    #============================================
    fp: Path = Path(fp)
    if not fp.exists(): raise FileExistsError(f"{fp} does not exist.")

    data: list = [] # To store the ctm in a list data structure

    #============================================
    # I should now fill the data list from the 
    # content in the file.
    #============================================
    # Open the txt file and read the content
    with open(str(fp), "r") as f:
      lines = [line.rstrip("\n") for line in f]

    # Store the lines of the text file in the annotation format
    for line in lines:
      start, end, label = line.split("\t")
      start, end = float(start), float(end)
      data.append((start, end, label, None, None))
    
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
    Annotation
      Loaded annotation object.
    """
    #============================================
    # I should raise error if the file does not
    # exist.
    #============================================
    fp: Path = Path(fp)
    if not fp.exists(): raise FileExistsError(f"{fp} does not exist.")

    data: list = []
    #============================================
    # I should now fill the data from the content
    # in the file.
    #============================================
    with open(str(fp), "r") as f:
      content = f.read().splitlines()
    
    for c in content:
      if not c.strip():
        continue
        
      parts = c.split()
      if len(parts) == 5:
        segment_id, channel, start, dur, label = parts
        start, dur = float(start), float(dur)
        confidence = None
          
      elif len(parts) == 6:
        segment_id, channel, start, dur, label, confidence = parts
        start, dur = float(start), float(dur)
        confidence = float(confidence)
      else:
        warnings.warn(f"'{c}' is not a standard ctm line.")
        continue
        
      data.append((start, start + dur, label, confidence, None))

    return ms.annotation(data)

  def textgrid(fp: Path|str):
    """
    Loads textgrid file as Annotation object.
    
    Parameters
    ----------
    fp: Path|str
      Filepath of the textgrid file.

    Returns
    -------
    Annotation
      Loaded annotation object.
    """
    #============================================
    # I should raise error if the file does not
    # exist.
    #============================================
    fp: Path = Path(fp)
    if not fp.exists(): raise FileExistsError(f"{fp} does not exist.")

    data: list = []
    #============================================
    # I should now fill the data from the content
    # in the file.
    #============================================
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
          in_interval = False  # ready for next interval
    
    return ms.annotation(data)
