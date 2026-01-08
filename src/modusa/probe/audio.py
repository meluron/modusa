# ---------------------------------
# Author: Ankit Anand
# File created on: 08-01-2026
# Email: ankit0.anand0@gmail.com
# ---------------------------------

import subprocess
import re
import imageio_ffmpeg as ffmpeg
from pathlib import Path

def audio(audiofp: str) -> dict:
    """
    Extract detailed audio info from an audio file using FFmpeg header.

    Parameters
    ----------
    audiofp : str
        Path to the audio file.

    Returns
    -------
    info : dict
        Dictionary containing audio properties:
        - codec: str
        - sr: int
        - channel_layout: str (mono/stereo)
        - duration: float (seconds)
        - bit_rate: int (bps)
        - format: str
    """

    audiofp: Path = Path(audiofp)
    if not audiofp.exists(): raise FileNotFoundError(f"{audiofp}")

    ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
    cmd = [ffmpeg_exe, "-i", str(audiofp)]
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    header = proc.stderr

    info = {}

    # Extract codec, sample rate, channels, channel layout
    m_audio = re.search(r'Audio:\s*([^,]+),\s*(\d+)\s*Hz,\s*(mono|stereo|[^,]+)', header)
    if m_audio:
        info['codec'] = m_audio.group(1).strip()
        info['sr'] = int(m_audio.group(2))
        channel_str = m_audio.group(3).strip()
        info['ch'] = channel_str
    else:
        raise RuntimeError(f"Could not parse audio info from header:\n{header}")

    # Extract duration
    m_dur = re.search(r'Duration:\s*(\d+):(\d+):(\d+\.?\d*)', header)
    if m_dur:
        hours, minutes, seconds = m_dur.groups()
        info['dur'] = int(hours) * 3600 + int(minutes) * 60 + float(seconds)
    else:
        info['dur'] = None

    # Extract overall bit rate (optional)
    m_bitrate = re.search(r'bitrate:\s*(\d+)\s*kb/s', header)
    if m_bitrate:
        info['bitrate'] = int(m_bitrate.group(1)) * 1000  # convert to bps
    else:
        info['bitrate'] = None

    # Extract format/container
    m_fmt = re.search(r'Input #0, ([^,]+),', header)
    if m_fmt:
        info['fmt'] = m_fmt.group(1).strip()
    else:
        info['fmt'] = None

    return info
