#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 06/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

from IPython.display import Audio, HTML, display
from pathlib import Path
import numpy as np
import base64

class AudioPlayer:
    
    def __init__(self):
        pass
        
    def play(y, sr, clip, label):
        """
        Audio player with optional clip selection, transcription-style label.
    
        Parameters
        ----------
        y: ndarray
            Audio signal.
        sr: int
            Sampling rate.
        clip: tuple[float, float] | None
            The portion from the audio signal to be played.
        label: str | None
            Could be transcription/labels attached to the audio.
        
        Returns
        -------
        None
        """
        start_time = 0.0
        end_time = len(y) / sr if y.ndim < 2 else y[0].size / sr
        
        # Optional clip selection
        if clip is not None:
            if not isinstance(clip, tuple) or len(clip) != 2:
                raise ValueError("`clip` must be a tuple of (start_time, end_time)")
            start_sample = int(clip[0] * sr)
            end_sample = int(clip[1] * sr)
            y = y[start_sample:end_sample]
            start_time, end_time = clip
            
            # Load and embed logo image as base64
        logo_path = Path(__file__).resolve().parent.parent / "images" / "icon.png"
        logo_size = 40
        logo_html = ""
        logo_link = "https://meluron.github.io/modusa"
        
        if logo_path.exists():
            with open(logo_path, "rb") as f:
                encoded_logo = base64.b64encode(f.read()).decode("utf-8")
                
                # Wrap logo in <a> so it's clickable
            logo_html = f"""
                <a href="{logo_link}" target="_blank" style="text-decoration:none;">
                    <img src="data:image/png;base64,{encoded_logo}"
                        style="
                            position:absolute;
                            bottom:8px;
                            right:10px;
                            width:{logo_size}px;
                            height:{logo_size}px;
                            opacity:0.8;
                            transition:opacity 0.2s ease;
                        "
                        onmouseover="this.style.opacity=1.0"
                        onmouseout="this.style.opacity=0.8"
                    />
                </a>
            """
        audio_html = Audio(data=y, rate=sr)._repr_html_()
        
        label_html = f"""
            <div style="
                margin-top:4px;
                padding:10px 12px;
                background:#f7f7f7;
                border-radius:6px;
                color:#222;
                font-size:14px;
                line-height:1.5;
            ">
                <strong>{start_time:.2f}s → {end_time:.2f}s:</strong>
                <span style="margin-left:6px;">{label if label else ''}</span>
            </div>
        """
        
        html = f"""
        <div style="
            display:inline-block;
            position:relative;
            border:1px solid #e0e0e0;
            border-radius:10px;
            padding:14px 18px 36px 18px;
            background:#fff;
            font-family:sans-serif;
            max-width:520px;
            box-shadow:0 1px 3px rgba(0,0,0,0.05);
        ">
            {label_html}
            <div style="margin-top:10px; margin-bottom:10px">
                {audio_html}
            </div>
            {logo_html}
        </div>
        """
        
        display(HTML(html))
        