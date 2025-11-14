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
    Datastructure to hold annotation.
    The format is [(start, end, label, confidence, group), (), ...]
    """
    
    def __init__(self, raw=None):
        self._raw = raw # Holds the raw data list[tuple[float, float, str, confidence, group]]
    
    def __repr__(self):
        lines = [f"{item}," for item in self._raw]
        return "Annotation(" + "[" + "\n".join(lines) + "])"
    
    def __len__(self):
        return len(self._raw)
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            # Return a new Annotation object with the sliced data
            return Annotation(self._raw[key])
        else:
            # Return a single element (tuple)
            return Annotation([self._raw[key]])
    def __iter__(self):
        return iter(self._raw)
    
    @staticmethod
    def _get_file_format(fp):
        """Return the format (str) of the file."""
        
        # Convert into path object
        fp: Path = Path(fp)
        
        # Extract the extension
        ext: str = fp.suffix
        
        return ext
    
    @staticmethod
    def _is_allowed_format(format):
        """
        Return True if the format is allowed to be loaded
        else False
        """
        
        ALLOWED_FORMAT: list = [".txt", ".ctm", ".textgrid"]
        
        return format in ALLOWED_FORMAT
    
    @staticmethod
    def _get_the_parser(format):
        """
        Return a function that can be used to parse the
        annotation format.
        """
        
        fmt2parser: dict = {".txt": Annotation._audacity_parser, ".ctm": Annotation._ctm_parser, ".textgrid": Annotation._textgrid_parser}
        
        return fmt2parser.get(format, None)
    
    @staticmethod
    def _audacity_parser(fp):
        """
        Parse audacity .txt label and return annotation.
        """
        
        with open(str(fp), "r") as f:
            lines = [line.rstrip("\n") for line in f]
            
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
        
    
    @staticmethod
    def _load(fp):
        """
        Load the annotation from a given filepath.
        """
        
        # Raise error if the file exists
        fp: Path = Path(fp)
        
        if not fp.exists():
            raise FileExistsError(f"{fp} does not exist.")
        
        # Find the format of the raw annotation file
        format: str = Annotation._get_file_format(fp)
        
        # Raise error if the format is allowed
        if not Annotation._is_allowed_format(format):
            raise ValueError(f"The annotation format is not allowed - {format}")
        
        # Get the correct parser for the annotation format to be loaded
        parser: Callable = Annotation._get_the_parser(format)
        
        # Load the annotation in raw format
        raw_annotation: list[tuple[float, float, str]] = parser(fp)
        
        # Create an Annotation object and store the raw annotation
        ann: Annotation = Annotation(raw_annotation)
            
        return ann
    
    # ==== Utility methods
    def trim(self, from_, to_):
        """
        Return a new annotation object trimmed to a segment.
        """
        raw_ann = [
            (start, end, label, confidence, group)
            for (start, end, label, confidence, group) in self._raw
            if start >= from_ and end <= to_
        ]
        return Annotation(raw_ann)


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
        
        return Annotation(new_raw_ann)
        

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

        return Annotation(new_raw_ann)
    
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
        
        return Annotation(new_raw_ann)
        
        
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

        