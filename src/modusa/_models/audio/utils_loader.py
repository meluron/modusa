#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 06/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import subprocess
import imageio_ffmpeg as ffmpeg
import re
    

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

if __name__ == "__main__":
   parse_sr_and_nchannels(audiofp="~/meluron/datasets/sample_songs/1.mp3")
