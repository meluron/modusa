from .. import probe

import subprocess
from pathlib import Path

import numpy as np
import imageio_ffmpeg as ffmpeg

def audio(audiofp: str, sr: int|None = None, ch: int|None = None) -> tuple[np.ndarray, int, str]:
    """
    Lightweight audio loader using imageio-ffmpeg.
    
    Parameters
    ----------
    audiofp: str | Path
      Path to the audio file.
    sr: int | None (default=None => Load in original sampling rate.)
      Sampling rate to load the audio in.
    ch: int | None (default=None => Load in original number of channels.)

    Returns
    -------
    np.ndarray
        Audio array with the content being loaded.
    int
        Sampling rate in which the content is loaded.
    str
        Filename for tracking.
    """

    audiofp: Path = Path(audiofp)
    if not audiofp.exists(): raise FileExistsError(f"{audiofp} does not exist")

    # 04-12-2025 [Ankit Anand]: Parse the sr and nchannels info from the header of the audio file and set the sr and ch to parsed values if not passed by user.
    header_info: dict = probe.audio(audiofp)
    if sr is None: sr = header_info['sr']
    if ch is None: ch = 2 if header_info['ch'] == "stereo" else 1
    
    # ============================================
    # 04-12-2025 [Ankit Anand]
    # I should load the audio array using FFMPEG 
    # executatable
    # ============================================
    ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
    
    cmd = [ffmpeg_exe]
    cmd += ["-i", str(audiofp), "-f", "s16le", "-acodec", "pcm_s16le"] # -f: s16le => raw PCM audio, no headers, -acodec: pcm_s16le => encode as uncompressed standard quality 
    cmd += ["-ar", str(sr)] # Setting the sampling rate to load the audio in.
    cmd += ["-ac", str(ch)] # Setting the number of channels to load the audio in.
    cmd += ["-"] # This tells ffmpeg to output the raw data into stdout that can be used to get the data without saving it.
    
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    raw = proc.stdout.read()
    proc.wait()
    
    # 04-12-2025 [Ankit Anand]: Convert the raw data into numpy array (normalized to have range between -1.0 and 1.0).
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    
    # For mono: (N) and for stereo: (2, N)
    if ch == 1: audio = np.array(audio)
    if ch == 2: audio = audio.reshape(-1, 2).T

    return audio, sr, audiofp.stem
