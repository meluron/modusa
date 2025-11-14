#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 06/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import pytest
import modusa as ms
from pathlib import Path

this_dir = Path(__file__).parents[0].resolve()

def test_load_audacity_txt():
	ann = ms.load.annotation(this_dir / "testdata/annotations/sample3.txt")

def test_load_ctm_1():
	ann = ms.load.annotation(this_dir / "testdata/annotations/sample1.ctm")

def test_load_ctm_2():
	ann = ms.load.annotation(this_dir / "testdata/annotations/sample2.ctm")