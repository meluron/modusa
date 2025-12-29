#!/usr/bin/env python3


from typing import Any
from pathlib import Path
import yt_dlp


def download(url, content_type, output_dir):
    """
    Downloads audio/video from YouTube.

    .. code-block:: python
        
        # To download audio
        import modusa as ms
        audio_fp = ms.download(
            url="https://www.youtube.com/watch?v=lIpw9-Y_N0g", 
            content_type="audio", 
            output_dir=".")
    
    Parameters
    ----------
    url: str
        Link to the YouTube video.
    content_type: str
        "audio" or "video"
    output_dir: str | Path
        Directory to save the YouTube content.
    
    Returns
    -------
    Path
        File path of the downloaded content.
    
    """
    if content_type == "audio":
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return Path(info['requested_downloads'][0]['filepath'])
        
    elif content_type == "video":
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # High quality
            'outtmpl': str(output_dir / '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': True,  # Hide verbose output
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return Path(info['requested_downloads'][0]['filepath'])
    else:
        raise ValueError(f"`content_type` can either take 'audio' or 'video' not {content_type}")
        
        
        