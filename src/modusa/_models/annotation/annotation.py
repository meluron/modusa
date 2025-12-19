#---------------------------------
# Author: Ankit Anand
# Date: 23-11-2025
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
    
  def __init__(self, data: list[tuple[float, float, str, float|None, int|None]]|None = None):
    self._data = data

  #============================================
  # Properties
  #============================================
  @property
  def data(self):
    return self._data

  @property
  def size(self):
    """Returns the total number of annotation entries"""
    return len(self)

  #============================================
  # Dunder methods
  #============================================  
  def __len__(self):
    """Returns total number of annotation entries."""
    return len(self.data)
    
  def __getitem__(self, key: slice | int):
    """Get item(s) from the annotation."""
    if isinstance(key, slice):
      # Return a new Annotation object with the sliced data
      return Annotation(self.data[key])
    else:
      # Return a single element (tuple) so that we can further unpack it
      return self.data[key]
        
  def __iter__(self):
    """Allows iteration over the annotation entries."""
    return iter(self.data)
  
  def __repr__(self):
    if self.size == 0:
      return "Annotation([])"
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
    
  #============================================
  # Trim feature.
  #============================================
  def trim(self, from_, to_):
    """
    Return a new annotation object trimmed to a segment.
    """
    raw_ann = [
        (start, end, label, confidence, group)
        for (start, end, label, confidence, group) in self.data
        if start >= from_ and end <= to_
    ]

    return Annotation(raw_ann)

  #============================================
  # Search feature.
  #============================================
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
    for (start, end, label, confidence, group) in self.data
    if regex_pattern.search(label)]
    
    return Annotation(new_raw_ann)
        
  #============================================
  # Group feature.
  #============================================
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
    for start, end, label, confidence, _ in self.data:
      group_num = None  # default
      # Loop through each regex pattern
      for i, pattern in enumerate(regex_patterns):
        # If the pattern matches, update the group number for that label
        if pattern.search(label):
          group_num = i
          break
      
      # After updating the group number, add it to the new annotation
      new_raw_ann.append((start, end, label, confidence, group_num))

    return Annotation(new_raw_ann)

  #============================================
  # Add entry feature
  #============================================
  def append(self, start: float, end: float, label: str, confidence: str|None = None, group: int|None = None):
    """
    Appends a new entry to the annotation data.

    Parameters
    ----------
    start: float
      Start time in sec.
    end: float
      End time in sec.
    label: str
      Label to attach with the entry to be added.
    confidence: float|None, default=None
      Confidence score of the label.
    group: int|None, default=None
      An group you would like to put the entry in.
      Useful during visualization.

    Returns
    -------
    None
    """
    self.data.append([start, end, str(label), confidence, group])

  #============================================
  # Remove entry feature.
  #============================================ 
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
      for (s, e, lbl, conf, grp) in self.data
      if not pattern.search(lbl)
    ]
    
    return Annotation(new_raw_ann)
    
  #============================================
  # Save in different formats.
  # text, ctm, textgrid
  #============================================
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
  ann = Annotation(data=[[0.0, 1.22110, "hello", 0.9, None], [1.5, 2.5, "world", 0.8, None]])
  ann.append(3, 5, "Test")
  print(ann.group(by_="*o*"))
  print(ann)
  print(Annotation(data=[]))
