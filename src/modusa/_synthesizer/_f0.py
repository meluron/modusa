#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 06/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import numpy as np

class F0Synthesizer:
    
    def __init__(self):
        pass
        
        
    @staticmethod
    def synthesize(f0, f0t, sr, nharm=0):
        """
        Synthesize f0 contour so that you can
        hear it back.
    
        Parameters
        ----------
        f0: ndarray
            Fundamental frequency (f0) contour in Hz.
        f0t: ndarray
            Timestamps in seconds
        sr: int
            Sampling rate in Hz for the synthesized audio.
        nharm: int
            Number of harmonics
            Default: 0 => Only fundamental frequency (No harmonics)
    
        Returns
        -------
        ndarray
            Syntesized audio.
        sr
            Sampling rate of the synthesized audio
        """
        
        # Create new time axis
        t = np.arange(0, f0t[-1], 1 / sr)
        
        # Interpolate the f0 to match the sampling time points
        f0_interp = np.interp(t, f0t, f0)
        
        # Compute phase by integrating frequency over time
        phase = 2 * np.pi * np.cumsum(f0_interp) / sr
        
        # Start with fundamental
        y = np.sin(phase)
        
        # Add harmonics if requested
        for n in range(2, nharm + 2):  # from 2nd to (nharm+1)th harmonic
            y += np.sin(n * phase) / n**2  # dividing by n to reduce harmonic amplitude
        
        # Normalize output to avoid clipping
        y /= np.max(np.abs(y))
        
        return y, sr
    
    