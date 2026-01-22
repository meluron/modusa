# ---------------------------------
# Author: Ankit Anand
# File created on: 22-01-2026
# Email: ankit0.anand0@gmail.com
# ---------------------------------

import numpy as np


def to_hz(midi, unvoiced_values=(0.0, -1.0, np.nan)):
    """
    Convert MIDI values to frequency in Hz, safely handling unvoiced frames.

    Parameters
    ----------
    midi : np.ndarray or float
        MIDI values
    unvoiced_values : tuple
        MIDI values that indicate unvoiced frames

    Returns
    -------
    f0 : np.ndarray or float
        Frequency in Hz
    """
    midi = np.asarray(midi, dtype=float)
    f0 = np.zeros_like(midi, dtype=float)

    voiced = np.ones_like(midi, dtype=bool)
    for uv in unvoiced_values:
        if np.isnan(uv):
            voiced &= ~np.isnan(midi)
        else:
            voiced &= midi != uv

    f0[voiced] = 440.0 * (2.0 ** ((midi[voiced] - 69.0) / 12.0))

    return f0
