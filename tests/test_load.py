#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 21/10/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import pytest
import modusa as ms
from pathlib import Path


#----------------------------------
# Loading different audio formats
#----------------------------------
this_dir = Path(__file__).parents[0].resolve()
def test_load_aac():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.aac")
	assert title == "sample"

def test_load_aiff():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.aiff")
	assert title == "sample"
	
def test_load_flac():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.flac")
	assert title == "sample"
	
def test_load_m4a():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.m4a")
	assert title == "sample"
	
def test_load_mp3():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.mp3")
	assert title == "sample"

def test_load_opus():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.opus")
	assert title == "sample"

def test_load_wav():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.wav")
	assert title == "sample"

#----------------------------------
# Resampe feature
#----------------------------------
SR = 16000 # Hz
def test_load_with_resample_aac():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.aac", sr=SR)
	assert sr == SR
	assert title == "sample"
	
def test_load_with_resample_aiff():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.aiff", sr=SR)
	assert sr == SR
	assert title == "sample"
	
def test_load_with_resample_flac():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.flac", sr=SR)
	assert sr == SR
	assert title == "sample"
	
def test_load_with_resample_m4a():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.m4a", sr=SR)
	assert sr == SR
	assert title == "sample"
	
def test_load_with_resample_mp3():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.mp3", sr=SR)
	assert sr == SR
	assert title == "sample"
	
def test_load_with_resample_opus():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.opus", sr=SR)
	assert sr == SR
	assert title == "sample"
	
def test_load_with_resample_wav():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.wav", sr=SR)
	assert sr == SR
	assert title == "sample"

#----------------------------------
# Trim feature
#----------------------------------
def test_load_with_trim_aac():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.aac", trim=(0, 5.3))
	assert title == "sample"
	
def test_load_with_trim_aiff():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.aiff", trim=(0, 5.3))
	assert title == "sample"
	
def test_load_with_trim_flac():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.flac", trim=(0, 5.3))
	assert title == "sample"
	
def test_load_with_trim_m4a():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.m4a", trim=(0, 5.3))
	assert title == "sample"
	
def test_load_with_trim_mp3():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.mp3", trim=(0, 5.3))
	assert title == "sample"
	
def test_load_with_trim_opus():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.opus", trim=(0, 5.3))
	assert title == "sample"
	
def test_load_with_trim_wav():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.wav", trim=(0, 5.3))
	assert title == "sample"

#----------------------------------
# Mono feature
#----------------------------------
def test_load_in_stereo_aac():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.aac", ch=2)
	assert y.ndim == 2
	assert title == "sample"
	
def test_load_in_stereo_aiff():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.aiff", ch=2)
	assert y.ndim == 2
	assert title == "sample"
	
def test_load_in_stereo_flac():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.flac", ch=2)
	assert y.ndim == 2
	assert title == "sample"
	
def test_load_in_stereo_m4a():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.m4a", ch=2)
	assert y.ndim == 2
	assert title == "sample"
	
def test_load_in_stereo_mp3():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.mp3", ch=2)
	assert y.ndim == 2
	assert title == "sample"
	
def test_load_in_stereo_opus():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.opus", ch=2)
	assert y.ndim == 2
	assert title == "sample"
	
def test_load_in_stereo_wav():
	y, sr, title = ms.load(this_dir / "testdata/audio-formats/sample.wav", ch=2)
	assert y.ndim == 2
	assert title == "sample"

#----------------------------------
# Load from YouTube
#----------------------------------
def test_load_youtube_1():
	y, sr, title = ms.load("https://www.youtube.com/watch?v=DIU_vmElPkU", ch=1)