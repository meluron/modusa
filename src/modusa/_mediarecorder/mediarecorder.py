#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 06/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

class MediaRecorder:
    
    def __init__(self):
        pass
        
    
    @staticmethod
    def mic():
        """
        Create a UI to record audio in jupyter notebook, the 
        recorded signal is available as array.
    
        .. code-block:: python
            
            import modusa as ms
            result = ms.record()
            y, sr, title = result() # Keep it in the next cell
    
        Returns
        -------
        Callable
            A lambda function that returns y(audio signal), sr(sampling rate), title(title set in the UI)
        """
        
        from ._mic import MicRecorder
        
        rec = MicRecorder.record()
        
        return rec