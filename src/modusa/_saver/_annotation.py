#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 08/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

from pathlib import Path

class AnnotationSaver:
    
    def __init__(self):
        pass
        
    @staticmethod
    def _audacity_label(ann, outfp):
        """
        Saves annotation as a text file.
        It can be opened in audacity for inspection.
    
        Paramters
        ---------
        ann: list[tuple[float, float, str]]
            - List of (start, end, label).
        outfp: str
            - Filepath to save the annotation.
        """
        output_fp = Path(outfp)
        output_fp.parent.mkdir(parents=True, exist_ok=True)
        
        with open(outfp, "w") as f:
            for (s, e, label, confidence, group) in ann:
                f.write(f"{s:.6f}\t{e:.6f}\t{label}\n")
                
    @staticmethod
    def _ctm_label(ann, outfp, segment_id, channel):
        """
        Saves annotation in CTM format.

        Parameters
        ----------
        ann: list[tuple[float, float, str]]
            List of (start, end, label).
        outfp: str
            Filepath to save the annotation.
        segment_id: str
            Segment/utterance ID.
        channel: int
            Audio channel.
        """
        output_fp = Path(outfp)
        output_fp.parent.mkdir(parents=True, exist_ok=True)
        
        with open(outfp, "w") as f:
            for (s, e, label, confidence, group) in ann:
                dur = e - s
                f.write(f"{segment_id} {channel} {s:.6f} {dur:.6f} {label} {confidence}\n")
                
    @staticmethod
    def _textgrid_label(ann, outfp, tier_name="labels"):
        """
        Saves annotation as a Praat TextGrid.

        Parameters
        ----------
        ann: list[tuple[float, float, str]]
            List of (start, end, label).
        outfp: str
            Filepath to save the annotation.
        tier_name: str
            Name of the TextGrid tier.
        """
        output_fp = Path(outfp)
        output_fp.parent.mkdir(parents=True, exist_ok=True)
        
        xmin = min(s for s, _, _, _, _ in ann) if ann else 0.0
        xmax = max(e for _, e, _, _, _ in ann) if ann else 0.0
        
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
            f.write(f"        intervals: size = {len(ann)}\n")
            
            for i, (s, e, label, confidence, group) in enumerate(ann, start=1):
                f.write(f"        intervals [{i}]:\n")
                f.write(f"            xmin = {s:.6f}\n")
                f.write(f"            xmax = {e:.6f}\n")
                f.write(f'            text = "{label}"\n')