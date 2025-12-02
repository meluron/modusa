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
	audio = ms.load.audio(this_dir / "testdata/audio-formats/sample.aac")
	assert audio.title == "sample"
	assert audio.size != 0
	assert audio.ch == 2
	assert audio.sr == 44100

def test_load_aiff():
	audio = ms.load.audio(this_dir / "testdata/audio-formats/sample.aiff")
	assert audio.title == "sample"
	assert audio.size != 0
	assert audio.ch == 2
	assert audio.sr == 44100
	
def test_load_flac():
	audio = ms.load.audio(this_dir / "testdata/audio-formats/sample.flac")
	assert audio.title == "sample"
	assert audio.size != 0
	assert audio.ch == 2
	assert audio.sr == 44100
	
def test_load_m4a():
	audio = ms.load.audio(this_dir / "testdata/audio-formats/sample.m4a")
	assert audio.title == "sample"
	assert audio.ch == 2
	assert audio.sr == 44100
	
def test_load_mp3():
	audio = ms.load.audio(this_dir / "testdata/audio-formats/sample.mp3")
	assert audio.title == "sample"
	assert audio.size != 0
	assert audio.ch == 2
	assert audio.sr == 44100

def test_load_opus():
	audio = ms.load.audio(this_dir / "testdata/audio-formats/sample.opus")
	assert audio.title == "sample"
	assert audio.size != 0
	assert audio.ch == 2
	assert audio.sr == 48000

def test_load_wav():
	audio = ms.load.audio(this_dir / "testdata/audio-formats/sample.wav")
	assert audio.title == "sample"
	assert audio.size != 0
	assert audio.ch == 2
	assert audio.sr == 44100
