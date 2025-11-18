#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 06/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

class Loader:
    """
    A namespace for loading different types
    of signal.

    Available methods:
    - audio
    - image
    - annotation
    """
    @staticmethod
    def audio(path, sr=None, trim=None, ch=None):
        """
        Lightweight audio loader using imageio-ffmpeg.
    
        Parameters
        ----------
        path: PathLike/str/URL
            - Path to the audio file / YouTube video
        sr: int
            - Sampling rate to load the audio in.
            - Default: None => Use the original sampling rate
        trim: tuple[number, number]
            - (start, end) in seconds to trim the audio clip.
            - Default: None => No trimming
        ch: int
            - 1 for mono and 2 for stereo
            - Default: None => Use the original number of channels.
    
        Returns
        -------
        np.ndarray
            - Audio signal Float32 waveform in [-1, 1].
        int:
            Sampling rate.
        str:
            File name stem.
        """
        
        from ._audio_loader import AudioLoader
        
        y, sr, title = AudioLoader.load(path, sr=sr, trim=trim, ch=ch)
        
        return y, sr, title
    
    @staticmethod
    def image(path):
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
        from ._image_loader import ImageLoader
        
        img = ImageLoader.load(path)
        
        return img
    
    @staticmethod
    def annotation(fp = None, raw: list[tuple[str, float, float, str, float]] = None):
        """
        Load annotation from audatity label
        text file, ctm label file, textgrid label file.
    
        Parameters
        ----------
        path: str | PathLike | None
            label text/ctm/textgrid file path.
        raw: list[tuple[str, float, float, str, float]] | None
            Pre-loaded raw annotation data structure
            [(start, end, label, confidence, group), (), ...]
    
        Returns
        -------
        Annotation
            Loaded Annotation object.
        """
        from ._annotation import Annotation
        
        if fp is not None:
            ann = Annotation._load_from_file(fp=fp)
        
        if raw is not None:
            ann = Annotation._load_from_raw(raw=raw)
        
        return ann
