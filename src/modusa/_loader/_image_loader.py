#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 06/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import imageio.v3 as iio
from pathlib import Path

class ImageLoader:
    """
    Loads image as numpy array.
    """
    def __init__(self):
        pass
        
    def load(path):
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
        
        path = Path(path)
        if not path.exists(): raise FileExistsError(f"{path} does not exist")
        
        img = iio.imread(path)
        
        return img