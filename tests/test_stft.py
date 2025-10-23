#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 23/10/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import pytest
import modusa as ms
import numpy as np

def test_stft():
	sr = 16000
	y = np.random.random(5*sr)
	S, Sf, St = ms.stft(y, sr)
