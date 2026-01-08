#---------------------------------
# Author: Ankit Anand
# Date: 20-11-2025
# Email: ankit0.anand0@gmail.com
#---------------------------------

import numpy as np
import modusa as ms
from pathlib import Path

#============================================
# Test loading audio of different file format
#============================================

this_dir = Path(__file__).parents[1].resolve()
def test_load_aac():
	y, sr, title = ms.load.audio(this_dir / "testdata/audio-formats/sample.aac")
	assert title == "sample"
	assert y.size != 0
	assert y.ndim == 2
	assert sr == 44100

def test_load_aiff():
	y, sr, title = ms.load.audio(this_dir / "testdata/audio-formats/sample.aiff")
	assert title == "sample"
	assert y.size != 0
	assert y.ndim == 2
	assert sr == 44100
	
def test_load_flac():
	y, sr, title = ms.load.audio(this_dir / "testdata/audio-formats/sample.flac")
	assert title == "sample"
	assert y.size != 0
	assert y.ndim == 2
	assert sr == 44100
	
def test_load_m4a():
	y, sr, title = ms.load.audio(this_dir / "testdata/audio-formats/sample.m4a")
	assert title == "sample"
	assert y.size != 0
	assert y.ndim == 2
	assert sr == 44100
	
def test_load_mp3():
	y, sr, title = ms.load.audio(this_dir / "testdata/audio-formats/sample.mp3")
	assert title == "sample"
	assert y.size != 0
	assert y.ndim == 2
	assert sr == 44100

def test_load_opus():
	y, sr, title = ms.load.audio(this_dir / "testdata/audio-formats/sample.opus")
	assert title == "sample"
	assert y.size != 0
	assert y.ndim == 2
	assert sr == 48000

def test_load_wav():
	y, sr, title = ms.load.audio(this_dir / "testdata/audio-formats/sample.wav")
	assert title == "sample"
	assert y.size != 0
	assert y.ndim == 2
	assert sr == 44100
