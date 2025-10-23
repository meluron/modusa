#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 23/10/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import pytest
import modusa as ms
from pathlib import Path

this_dir = Path(__file__).parents[0].resolve()

def test_save_ann():
	ann = [(0, 1, "Label 1"), (1.2, 5, "Label 2")]
	
	ms.save_ann(ann, output_fp=this_dir / "testdata" / "tmp" / "ann.txt")
