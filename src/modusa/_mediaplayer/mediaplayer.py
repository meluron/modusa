#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 06/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------


class MediaPlayer:
    
    def __init__(self):
        pass
        
    def audio(y, sr, clip=None, label=None):
        """
        Audio player with optional clip selection, transcription-style label.
    
        Parameters
        ----------
        y: ndarray
            - Audio signal.
        sr: int
            - Sampling rate.
        clip: tuple[float, float] | None
            - The portion from the audio signal to be played.
        label: str | None
            - Could be transcription/labels attached to the audio.
        
        Returns
        -------
        None
        """
        
        from ._audio import AudioPlayer
        
        AudioPlayer.play(y, sr, clip, label)