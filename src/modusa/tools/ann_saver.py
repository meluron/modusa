#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 23/10/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

from pathlib import Path

def save_ann(ann, output_fp):
	"""
	Saves annotation as a text file.
	It can be opened in audacity for inspection.

	Paramters
	---------
	ann: list[tuple[float, float, str]]
		- List of (start, end, label).
	output_fp: str
		- Filepath to save the annotation.
	"""
	
	output_fp = Path(output_fp)
	output_fp.parent.mkdir(parents=True, exist_ok=True)
	
	with open(output_fp, "w") as f:
		for (s, e, label) in ann:
			f.write(f"{s:.6f}\t{e:.6f}\t{label}\n")
	