#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 06/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import subprocess
import numpy as np
import imageio_ffmpeg as ffmpeg
from pathlib import Path
import re

class AudioLoader:
    """
    Loads audio signal as numpy array.
    """
    def __init__(self):
        pass
        
    @staticmethod
    def _read_header(path: Path, ffmpeg_exe):
        """
        Get header text from audio to extract useful
        parameters.
    
        Parameters
        ----------
        audiofp: PathLike
            - Audio filepath
        
        Returns
        -------
        int
            - Original sampling rate (hz)
        int
            - Number of channels
        """
        
        cmd = [ffmpeg_exe, "-i", str(path)]
        proc = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        text = proc.stderr
        
        return text	
    
    @staticmethod
    def _parse_sr_and_nchannels(header_txt: str):
        """
        Given the header text of audio, parse
        the audio sampling rate and number of
        channels.

        Parameters
        ----------
        header_txt: str
            Extracted header text of the audio.

        Returns
        -------
        int
            Sampling rate.
        int
            Number of channels (1 or 2)
        """
        
        m = re.search(r'Audio:.*?(\d+)\s*Hz.*?(mono|stereo)', header_txt) # "Stream #0:0: Audio: mp3, 44100 Hz, stereo, ..."
        if not m:
            raise RuntimeError("Could not parse audio info")
        sr = int(m.group(1))
        channels = 1 if m.group(2) == "mono" else 2
        
        return sr, channels
    
    @staticmethod
    def load(path, sr: int, trim: tuple[float, float], ch: int):
        """
        Lightweight audio loader using imageio-ffmpeg.
    
        Parameters
        ----------
        path: PathLike | str
            Path to the audio file
        sr: int
            Sampling rate to load the audio in.
            Default: None => Use the original sampling rate
        trim: tuple[number, number]
            (start, end) in seconds to trim the audio clip.
            Default: None => No trimming
        ch: int
            1 for mono and 2 for stereo
            Default: None => Use the original number of channels.
    
        Returns
        -------
        np.ndarray
            Audio signal Float32 waveform in [-1, 1].
        int:
            Sampling rate.
        str:
            File name stem.
        """
        path = Path(path)
        
        if not path.exists(): raise FileExistsError(f"{path} does not exist")
        
        # Get the FFMPEG executable
        ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
        
        # Read the header
        header: str = AudioLoader._read_header(path, ffmpeg_exe)
        
        # Parse the sr and nchannels info from the header
        default_sr, default_nchannels = AudioLoader._parse_sr_and_nchannels(header) # int, int
        
        # Use the parsed sr and nchannels if not explicitely passed by the user
        if sr is None: sr = default_sr
        if ch is None: ch = default_nchannels
        
        cmd = [ffmpeg_exe]
        
        # Optional trimming
        if trim is not None:
            start, end = trim
            duration = end - start
            cmd += ["-ss", str(start), "-t", str(duration)]
            
        cmd += ["-i", str(path), "-f", "s16le", "-acodec", "pcm_s16le"]
        cmd += ["-ar", str(sr)]
        cmd += ["-ac", str(ch)]
        
        cmd += ["-"]
        
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        raw = proc.stdout.read()
        proc.wait()
        
        audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
        
        # Stereo reshaping if forced
        if ch == 2:
            audio = audio.reshape(-1, 2).T
            
        return audio, sr, path.stem
    