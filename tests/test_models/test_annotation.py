#---------------------------------
# Author: Ankit Anand
# Date: 19-11-2025
# Email: ankit0.anand0@gmail.com
#---------------------------------

import modusa as ms
from pathlib import Path

this_dir = Path(__file__).parents[1].resolve()

data = [(1, 2, "Label 1", None, None), (5, 6, "Label 2", 0.5, 1)]

# Test loading annotation object from different sources
def test_load_audacity_txt():
	ann = ms.load.audacity_label(this_dir / "testdata/annotations/sample3.txt")

def test_load_ctm_with_5_cols():
	# This has 5 columns (no confidence column)
	ann = ms.load.ctm(this_dir / "testdata/annotations/sample1.ctm")

def test_load_ctm_with_6_cols():
	# This has 6 columns (with confidence column)
	ann = ms.load.ctm(this_dir / "testdata/annotations/sample2.ctm")

def test_load_textgrid():
	pass

def test_load_raw():
	ann = ms.annotation(data)

def test_load_empty():
	ann = ms.annotation([])

def test_get_item():
	ann = ms.annotation(data=data)
	assert ann[0] == data[0]

def test_len():
	ann = ms.annotation(data=data)
	assert len(ann) == ann.size == 2
