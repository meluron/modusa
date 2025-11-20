#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 11/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

from typing import Callable
from pathlib import Path
import warnings
from copy import deepcopy
import re

class Annotation:
  """
  A modusa model class for annotation for audio data.
  
  Annotation wraps around
  [[start_time, end_time, label, confidence, group], ...]
  """
    
  def __init__(self, annfp: str | Path | None = None, raw: list[tuple[float, float, str, float | None, int | None]] | None = None):
    # Intantiate the annotaton object
    # == If annfp is passed, load from the file
    if annfp is not None:
      if not isinstance(annfp, str | Path):
        raise ValueError(f"'fp' must be either str or Path, not {type(annfp)}")
      self._load_from_file(annfp=annfp)
    # == If raw data [[[start, end, label, confidence, group]]] is passed, load from the raw data
    elif raw is not None:
      self._load_from_raw(raw=raw)
    # == Raise error if neither is passed
    else:
      raise ValueError("Either 'fp' or 'raw' must be provided to load the annotation.")

  def __repr__(self):
    # To have a string representation of the annotation object Annotation([[start, end, label, confidence, group], [...], ...]])
    entries_str = [] # List of entries with each entry being another list [start end label confidence group]
    
    # Fill the entries_str list
    # == Add comma between elements of each entry [start end label confidence group] -> [start, end, label, confidence, group]
    for entry in self:
        entry_str = ", ".join(str(element) for element in entry)
        entries_str.append(f"({entry_str})")
    
    # Combine all entries into the final string representation with indentation for each entry
    indent = "  "  # Indentation for each line
    return f"Annotation([\n{indent}" + f"\n{indent}".join(entries_str) + "\n])"
    
  def __len__(self):
    """Returns total number of annotation entries."""
    return len(self._raw)

  @property
  def size(self):
    """Returns the total number of annotation entries"""
    return len(self)
    
  def __getitem__(self, key: slice | int):
    """Get item(s) from the annotation."""
    if isinstance(key, slice):
      # Return a new Annotation object with the sliced data
      return Annotation(raw=self._raw[key])
    else:
      # Return a single element (tuple) so that we can further unpack it
      return self._raw[key]
        
  def __iter__(self):
    """Allows iteration over the annotation entries."""
    return iter(self._raw)
    
  @staticmethod
  def _get_the_parser(fp):
    """
    Return a function that can be used to parse the
    annotation file in supported fornats.
    """
    SUPPORTED_FORMATS: list = [".txt", ".ctm", ".textgrid"]

    # Convert into path object
    fp: Path = Path(fp) 
    # Extract the extension
    format: str = fp.suffix

    if format not in SUPPORTED_FORMATS:
      raise ValueError(f"The annotation format is not supported - {fp}")
    else:
      fmt2parser: dict = {".txt": Annotation._audacity_parser, ".ctm": Annotation._ctm_parser, ".textgrid": Annotation._textgrid_parser}
    
    return fmt2parser.get(format, None)
    
  @staticmethod
  def _audacity_parser(fp):
    """
    Parse audacity .txt label and return annotation.
    """
    # Open the txt file and read the content
    with open(str(fp), "r") as f:
      lines = [line.rstrip("\n") for line in f]

    # Store the lines of the text file in teh annotation format 
    ann = []
    for line in lines:
      start, end, label = line.split("\t")
      start, end = float(start), float(end)
      ann.append((start, end, label, None, None))
            
    return ann
    
  @staticmethod
  def _ctm_parser(fp):
    """
    Parse .ctm label and return annotation.
    """
    with open(str(fp), "r") as f:
      content = f.read().splitlines()
    
    ann = []
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
        
      ann.append((start, start + dur, label, confidence, None))
    
    return ann
    
  @staticmethod
  def _textgrid_parser(fp, trim):
    """
    Parse .textgrid label and return annotation.
    """
    ann = []
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
            ann.append((s, e, label, None, None))
          in_interval = False  # ready for next interval
                
    return ann
        
  def _load_from_file(self, annfp: Path):
    """
    Load the annotation from a given filepath.
    """
      
    # Raise error if the file does not exist
    annfp: Path = Path(annfp)
    if not annfp.exists():
      raise FileExistsError(f"{annfp} does not exist.")
    
    # Get the correct parser for the given annotation format
    parser: Callable = Annotation._get_the_parser(annfp)

    # Parse the raw annotation using the correct parser
    raw_annotation: list[tuple[float, float, str]] = parser(annfp)

    # Store the raw annotation in the annotation object
    self._raw = raw_annotation
  
    return self

  def _load_from_raw(self, raw: list[tuple[str, float, float, str, float], ...]):
    """
    Load the annotation from a given raw data structure.
    """
    self._raw = raw
    return self
    
  # ==== Utility methods for annotation object
  def trim(self, from_, to_):
    """
    Return a new annotation object trimmed to a segment.
    """
    raw_ann = [
        (start, end, label, confidence, group)
        for (start, end, label, confidence, group) in self._raw
        if start >= from_ and end <= to_
    ]

    return Annotation(raw=raw_ann)


  def search(self, for_: str, case_insensitive: bool = True):
    """
    Return a new annotation object with the
    label that matches to the search query.

    Custom pattern:
        *L  => label ends with 'L'
        L*  => label starts with 'L'
        *L* => label contains 'L'
        L   => label exactly equals 'L'
    """
    
    # Setup the variables
    pattern: str = for_
    new_raw_ann = []
    case_sensitivity_flag = re.IGNORECASE if case_insensitive else 0
        
    if pattern.startswith("*") and pattern.endswith("*"):
      regex_pattern = re.compile(re.escape(pattern.strip("*")), case_sensitivity_flag)
    elif pattern.startswith("*"):
      regex_pattern = re.compile(re.escape(pattern.strip("*")) + r"$", case_sensitivity_flag)
    elif pattern.endswith("*"):
      regex_pattern = re.compile(r"^" + re.escape(pattern.strip("*")), case_sensitivity_flag)
    else:
      regex_pattern = re.compile('^' + re.escape(pattern) + '$', case_sensitivity_flag)
    
    # Loop through each label
    new_raw_ann = [(start, end, label, confidence, group)
    for (start, end, label, confidence, group) in self._raw
    if regex_pattern.search(label)]
    
    return Annotation(raw=new_raw_ann)
        

  def group(self, by_: str | list[str, ...],  case_insensitive: bool = True):
    """
    Return a new Annotation object containing entries whose label matches the given pattern(s).

    Custom pattern:
        *L  => label ends with 'L'
        L*  => label starts with 'L'
        *L* => label contains 'L'
        L   => label exactly equals 'L'
    """
    
    # Setup the variables
    patterns: str = by_
    new_raw_ann = []
    case_sensitivity_flag = re.IGNORECASE if case_insensitive else 0
    
    # Standerdize the input to be a list
    if isinstance(patterns, str): patterns = [patterns]
    
    new_raw_ann = [] # To store the new raw annotation
    
    # Convert our custom patterns to regex patterns format
    regex_patterns = []
    for pattern in patterns:
      if pattern.startswith("*") and pattern.endswith("*"):
        regex_pattern = re.compile(re.escape(pattern.strip("*")), case_sensitivity_flag)
      elif pattern.startswith("*"):
        regex_pattern = re.compile(re.escape(pattern.strip("*")) + r"$", case_sensitivity_flag)
      elif pattern.endswith("*"):
        regex_pattern = re.compile(r"^" + re.escape(pattern.strip("*")), case_sensitivity_flag)
      else:
        regex_pattern = re.compile('^' + re.escape(pattern) + '$', case_sensitivity_flag)
      regex_patterns.append(regex_pattern)
    
    # Loop through each label
    for start, end, label, confidence, _ in self._raw:
      group_num = None  # default
      # Loop through each regex pattern
      for i, pattern in enumerate(regex_patterns):
        # If the pattern matches, update the group number for that label
        if pattern.search(label):
          group_num = i
          break
      
      # After updating the group number, add it to the new annotation
      new_raw_ann.append((start, end, label, confidence, group_num))

    return Annotation(raw=new_raw_ann)
    
  def remove(self, this_: str, case_insensitive: bool = True):
    """
    Returns a new annotation object after removing
    all labels that match the given pattern.
    
    Custom pattern:
        *L  => label ends with 'L'
        L*  => label starts with 'L'
        *L* => label contains 'L'
        L   => label exactly equals 'L'
    """
    
    # Choose regex flags
    case_sensitivity_flag = re.IGNORECASE if case_insensitive else 0
    
    # Convert wildcard to regex
    if this_.startswith("*") and this_.endswith("*"):
      pattern = re.compile(re.escape(this_.strip("*")), case_sensitivity_flag)
    elif this_.startswith("*"):
      pattern = re.compile(re.escape(this_.strip("*")) + r"$", case_sensitivity_flag)
    elif this_.endswith("*"):
      pattern = re.compile(r"^" + re.escape(this_.strip("*")), case_sensitivity_flag)
    else:
      pattern = re.compile("^" + re.escape(this_) + "$", case_sensitivity_flag)
    
    # Filter out matches
    new_raw_ann = [
      (s, e, lbl, conf, grp)
      for (s, e, lbl, conf, grp) in self._raw
      if not pattern.search(lbl)
    ]
    
    return Annotation(raw=new_raw_ann)
        
        
  def to_list(self):
    """
    Converts the annotation into list format.
    """
    return deepcopy(self._raw)
    
  # ======
  # Save annotation in differnt format
  # ======    
  def saveas_txt(self, outfp):
    """
    Saves annotation as a text file.
    It can be opened in audacity for inspection.

    Paramters
    ---------
    outfp: str
        - Filepath to save the annotation.
    """
    output_fp = Path(outfp)
    output_fp.parent.mkdir(parents=True, exist_ok=True)
    
    with open(outfp, "w") as f:
      for (s, e, label, confidence, group) in self:
        f.write(f"{s:.6f}\t{e:.6f}\t{label}\n")
                
  def saveas_ctm(self, outfp, segment_id="utter_1", channel=1):
    """
    Saves annotation in CTM format.

    Parameters
    ----------
    outfp: str
        Filepath to save the annotation.
    segment_id: str, default="utter_1"
        Segment/utterance ID.
    channel: int, default=1
        Audio channel.
    """
    output_fp = Path(outfp)
    output_fp.parent.mkdir(parents=True, exist_ok=True)
    
    with open(outfp, "w") as f:
      for (s, e, label, confidence, group) in self:
        dur = e - s
        f.write(f"{segment_id} {channel} {s:.6f} {dur:.6f} {label} {confidence}\n")
                
  def saveas_textgrid(self, outfp, tier_name="labels"):
    """
    Saves annotation as a Praat TextGrid.

    Parameters
    ----------
    ann: list[tuple[float, float, str]]
        List of (start, end, label).
    outfp: str
        Filepath to save the annotation.
    tier_name: str, default="labels"
        Name of the TextGrid tier.
    """
    output_fp = Path(outfp)
    output_fp.parent.mkdir(parents=True, exist_ok=True)
    
    xmin = min(s for s, _, _, _, _ in self) if self else 0.0
    xmax = max(e for _, e, _, _, _ in self) if self else 0.0
    
    with open(outfp, "w") as f:
      f.write('File type = "ooTextFile"\n')
      f.write('Object class = "TextGrid"\n\n')
      f.write(f"xmin = {xmin:.6f}\n")
      f.write(f"xmax = {xmax:.6f}\n")
      f.write("tiers? <exists>\n")
      f.write("size = 1\n")
      f.write(f"item []:\n")
      f.write("    item [1]:\n")
      f.write('        class = "IntervalTier"\n')
      f.write(f'        name = "{tier_name}"\n')
      f.write(f"        xmin = {xmin:.6f}\n")
      f.write(f"        xmax = {xmax:.6f}\n")
      f.write(f"        intervals: size = {len(self)}\n")
      
      for i, (s, e, label, confidence, group) in enumerate(self, start=1):
        f.write(f"        intervals [{i}]:\n")
        f.write(f"            xmin = {s:.6f}\n")
        f.write(f"            xmax = {e:.6f}\n")
        f.write(f'            text = "{label}"\n')


if __name__ == "__main__":
  ann = Annotation(raw=[[0.0, 1.22110, "hello", 0.9, None], [1.5, 2.5, "world", 0.8, None]])
  print(ann.group(by_="*o*"))
  print(ann)
