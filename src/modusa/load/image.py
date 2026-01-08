from pathlib import Path

import numpy as np
import imageio.v3 as iio

def image(imagefp: str) -> np.ndarray:
    """
    Loads an images using imageio.

    Parameters
    ----------
    path: str | PathLike
        Image file path.
    
    Returns
    -------
    np.ndarray
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
