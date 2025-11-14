#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 06/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

class FeatureExtractor:
    """
    A namespace for extracting various features
    from the loaded signal.

    Available methods:
    - stft
    """
    
    @staticmethod
    def stft(y, sr, winlen=None, hoplen=None, gamma=None):
        """
        Compute spectrogram with just numpy.
    
        Parameters
        ----------
        y: ndarray
            Audio signal.
        sr: int
            Sampling rate of the audio signal.
        winlen: int
            Window length in samples.
            Default: None => set at 0.064 sec
        hoplen: int
            Hop length in samples.
            Default: None => set at one-forth of winlen
        gamma: int | None
            Log compression factor.
            Add contrast to the plot.
            Default: None
    
        Returns
        -------
        ndarray:
            Spectrogram matrix, complex is gamma is None else real
        ndarray:
            Frequency bins in Hz.
        ndarray:
            Timeframes in sec.
        """
        
        from ._stft import STFTExtractor
        
        X, Xf, Xt = STFTExtractor.extract(y, sr, winlen, hoplen, gamma)
        
        return X, Xf, Xt