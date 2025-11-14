#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 06/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

class Synthesizer:
    
    @staticmethod
    def pitch(f0, f0t, sr, nharm=0):
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
        
        from ._f0 import F0Synthesizer
        
        y, sr = F0Synthesizer.synthesize(f0, f0t, sr, nharm)
        
        return y, sr
    
    @staticmethod
    def clicks(onsets, sr, freq=1000, click_duration=0.03, size=None, strengths=None):
        
        """
        Synthesize a metronome-like click train with optional per-click strengths.
    
        Parameters
        ----------
        onsets : array-like
            Times of clicks in seconds.
        sr : int
            Sample rate.
        freq : float
            Frequency of the click sound (Hz).
        click_duration : float
            Duration of each click in seconds.
        size : int or None
            Length to trim/pad the final output (in samples). If None, determined from onsets.
        strengths : array-like or None
            Relative amplitude of each click (same length as `onsets`).
            If None, all clicks are equal in strength (1.0).
    
        Returns
        -------
        np.ndarray
            Audio signal with sine wave clicks at event times.
        int
            Sampling rate of the generated click audio.
        """
        
        from ._onsets import OnsetsSynthesizer
        
        y, sr = OnsetsSynthesizer.synthesize(onsets, sr, freq, click_duration, size, strengths)
        
        return y, sr