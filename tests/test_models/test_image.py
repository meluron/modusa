#---------------------------------
# Author: Ankit Anand
# Date: 20-11-2025
# Email: ankit0.anand0@gmail.com
#---------------------------------

import pytest
import modusa as ms
from pathlib import Path

#============================================
# Test loading image from different image
# file format.
#============================================
this_dir = Path(__file__).parents[1].resolve()
def test_load_image_1():
  img = ms.image(imagefp=this_dir / "testdata/images" / "1.png")
  assert img.ndim == 3
  assert img.size != 0

def test_load_image_2():
  img = ms.image(imagefp=this_dir / "testdata/images" / "2.png")
  assert img.ndim == 3
  assert img.size != 0
