#!/usr/bin/env python3


import subprocess
from pathlib import Path

def convert(inp_audio_fp, output_audio_fp, sr = None, mono = False) -> Path:
    """
    Converts an audio file from one format to another using FFmpeg.

    .. code-block:: python
        
        import modusa as ms
        converted_audio_fp = ms.convert(
            inp_audio_fp="path/to/input/audio.webm", 
            output_audio_fp="path/to/output/audio.wav")

    Parameters
    ----------
    inp_audio_fp: str | Path
        - Filepath of audio to be converted.
    output_audio_fp: str | Path
        - Filepath of the converted audio. (e.g. name.mp3)
    sr: int | float
        - Resample it to any target sampling rate.
        - Default: None => Keep the original sample rate.
    mono: bool
        - Do you want to convert the audio into mono?
        - Default: False

    Returns
    -------
    Path:
        Filepath of the converted audio.

    Note
    ----
    - The conversion takes place based on the extensions of the input and output audio filepath.
    """
    inp_audio_fp = Path(inp_audio_fp)
    output_audio_fp = Path(output_audio_fp)
    
    if not inp_audio_fp.exists():
        raise FileNotFoundError(f"`inp_audio_fp` does not exist, {inp_audio_fp}")
        
    if inp_audio_fp == output_audio_fp:
        raise ValueError(f"`inp_fp` and `output_fp` must be different")
        
    output_audio_fp.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(inp_audio_fp),
        "-vn",  # No video
    ]
    
    # Optional sample rate
    if sr is not None:
        cmd += ["-ar", str(sr)]
        
        # Optional mono
    if mono is True:
        cmd += ["-ac", "1"]
        
    cmd.append(str(output_audio_fp))
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        raise RuntimeError(f"FFmpeg failed to convert {inp_audio_fp} to {output_audio_fp}")
        
    return output_audio_fp