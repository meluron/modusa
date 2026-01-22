# ---------------------------------
# Author: Ankit Anand
# File created on: 22-01-2026
# Email: ankit0.anand0@gmail.com
# ---------------------------------

import numpy as np

def to_midi(f0, unvoiced_value=0.0, ref=440.0):
    """
    Convert frequency in Hz to MIDI, safely handling unvoiced frames.

    Parameters
    ----------
    f0 : np.ndarray or float
        Frequency in Hz
    unvoiced_value : float
        Value to assign to unvoiced frames (default: 0.0)
    ref: float
        Reference note (default: 440.0) Standard A4

    Returns
    -------
    midi : np.ndarray or float
        MIDI values
    """
    f0 = np.asarray(f0, dtype=float)
    midi = np.full_like(f0, unvoiced_value, dtype=float)

    voiced = f0 > 0
    midi[voiced] = 69.0 + 12.0 * np.log2(f0[voiced] / ref)

    return midi
