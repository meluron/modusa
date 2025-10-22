#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 22/10/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import pytest
import modusa as ms
import numpy as np

def test_synth_f0():
	sr = 16000
	y, sr = ms.synth_f0(np.zeros(int(5*sr)), np.arange(5*sr) / sr, 16000, 0)
