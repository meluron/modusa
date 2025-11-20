#---------------------------------
# Author: Ankit Anand
# Date: 20-11-2025
# Email: ankit0.anand0@gmail.com
#---------------------------------

import imageio.v3 as iio
from pathlib import Path
import numpy as np

class Image:
  """
  """

  def __init__(self, imagefp: str|Path):

    #============================================
    # List all the interal state for easier 
    # remeberance
    #============================================
    self._M = None

    #============================================
    # Load the image and update the state
    #============================================
    M: np.ndarray = Image._load_from_file(imagefp=imagefp)
    self._M = M

  @property
  def M(self):
    return self._M
  
  @property
  def size(self):
    return self.M.size
  
  @property
  def shape(self):
    return self.M.shape
  
  @property
  def ndim(self):
    return self.M.ndim
  
  def __array__(self, copy=True):
    return self.M

  @staticmethod
  def _load_from_file(imagefp: str|Path):
    """
    Loads an images using imageio.

    Parameters
    ----------
    path: str | PathLike
        Image file path.
    
    Returns
    -------
    ndarray
        Image array (2D/3D with RGB channel)
    """
    
    #============================================
    # If the file does not exist, raise error
    # else try loading the image using iio
    #============================================
    imagefp = Path(imagefp)
    if not imagefp.exists(): 
      raise FileExistsError(f"{imagefp} does not exist")
    else:
      img = iio.imread(imagefp)
    
    return img
