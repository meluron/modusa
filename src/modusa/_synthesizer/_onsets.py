#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 06/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import numpy as np

class OnsetsSynthesizer:
    
    def __init__(self):
        pass
        
    @staticmethod
    def synthesize(onsets, sr, freq, click_duration, size=None, strengths=None):
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
        t_click = np.linspace(0, click_duration, int(sr * click_duration), False)
        
        # Base click tone
        click = np.sin(2 * np.pi * freq * t_click)
        
        # Apply exponential decay envelope for a percussive feel
        click *= np.exp(-15 * t_click)
        
        # Determine output length
        if size is None:
            size = int(np.ceil((max(onsets) + click_duration) * sr))
            
        y = np.zeros(size)
        
        # Handle strengths
        if strengths is None:
            strengths = np.ones_like(onsets, dtype=float)
        else:
            strengths = np.array(strengths, dtype=float)
            strengths = np.clip(strengths, 0, None)  # remove negatives
            if np.max(strengths) > 0:
                strengths /= np.max(strengths)
            assert len(strengths) == len(onsets), "strengths must match onsets in length"
            
            # Place clicks at specified onsets
        for onset, strength in zip(onsets, strengths):
            start = int(onset * sr)
            end = start + len(click)
            if end > size:
                end = size
            y[start:end] += strength**2 * click[:end-start]
            
        # Normalize
        y /= np.max(np.abs(y)) + 1e-10
        
        return y, sr
    