#---------------------------------
# Author: Ankit Anand
# Date: 02-12-2025
# Email: ankit0.anand0@gmail.com
#---------------------------------

from pathlib import Path
import warnings
from .annotation import Annotation

def load_audacity_labeltext(fp: Path|str):
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
  
  return Annotation(data)


def load_ctm(fp: Path|str):
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

  return Annotation(data)


def load_textgrid(fp: Path|str):
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
  
  return Annotation(data)
