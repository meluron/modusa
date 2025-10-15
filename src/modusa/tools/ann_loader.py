#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 12/08/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

def load_ann(path, clip=None):
	"""
	Load annotation from audatity label
	text file and also ctm file.

	Parameters
	----------
	path: str
		- label text/ctm file path.
	clip: tuple[number, number] | number | None
		- Incase you clipped the audio signal, this parameter will help clip the annotation.
		- If you clip the audio, say from (10, 20), set the clip to (10, 20).
		- Default: None

	Returns
	-------
	list[tuple, ...]
		- annotation data structure
		- [(start, end, label), ...]
	"""
	from pathlib import Path
	
	if not isinstance(path, (str, Path)):
		raise ValueError(f"`path` must be one of (str, Path), got {type(path)}")
	
	# Convert to Path object
	path = Path(path)
	
	# Check if the path exists
	if not path.exists():
		raise FileExistsError(f"{path} does not exist")
		
	ann = [] # This will store the annotation
	
	# Clipping the annotation to match with the clipped audio
	if clip is not None:
		# Map clip input to the right format
		if isinstance(clip, int or float):
			clip = (0, clip)
		elif isinstance(clip, tuple) and len(clip) > 1:
			clip = (clip[0], clip[1])
		else:
			raise ValueError(f"Invalid clip type or length: {type(clip)}, len={len(clip)}")
	
	if path.suffix == ".txt":
		with open(str(path), "r") as f:
			lines = [line.rstrip("\n") for line in f]
			for line in lines:
				start, end, label = line.split("\t")
				start, end = float(start), float(end)
				
				# Incase user has clipped the audio signal, we adjust the annotation
				# to match the clipped audio
				if clip is not None:
					offset = clip[0]
					# Clamp annotation to clip boundaries
					new_start = max(start, clip[0]) - offset
					new_end   = min(end, clip[1]) - offset
					
					# only keep if there's still overlap
					if new_start < new_end:
						ann.append((new_start, new_end, label))
				else:
					ann.append((start, end, label))
					
	elif path.suffix == ".ctm":
		with open(str(path), "r") as f:
			content = f.read().split("\n")
			
		for c in content:
			c = c.strip()
			if c == "": # Handle empty line usually at the end of the ctm file
				continue
			elif len(c.split(" ")) != 5:
				warnings.warn(f" '{c}' is not a standard ctm line.")
			if len(c.split(" ")) == 5:
				_, _, start, dur, label = c.split(" ")
				start, dur = float(start), float(dur)
				end = start + dur
				
				# Incase user has clipped the audio signal, we adjust the annotation
				# to match the clipped audio
				if clip is not None:
					offset = clip[0]
					# Clamp annotation to clip boundaries
					new_start = max(start, clip[0]) - offset
					new_end   = min(end, clip[1]) - offset
					
					# only keep if there's still overlap
					if new_start < new_end:
						ann.append((new_start, new_end, label))
				else:
					ann.append((start, end, label))
				
	else:
		raise Exception(f"Unsupported file type {path.suffix}")
	return ann