#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 09/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

from io import BytesIO
from IPython.display import HTML, display
import base64
import imageio.v2 as imageio
import matplotlib.pyplot as plt
from pathlib import Path

class Animator:
    """
    A context-managed animation builder.

    Parameters
    ----------
    path : str
        Output file path (e.g. "wave.gif")
    fps: int
        - Frames per second of the output animation
        - Default: 8
    pad: float
        - Padding (inches) around each frame to give consistent breathing space
        - Default: 0.4
    facecolor: str
        - Background color for each frame
        - Default: "white"
    """
    
    def __init__(self, path, fps=8, pad=0.4, facecolor="white", loop=True):
        self._path = path
        self._fps = fps
        self._pad = pad
        self._facecolor = facecolor
        self._loop = loop
        self._frames = []
        
    def __enter__(self):
        return self
    
    def snapshot(self, fig):
        """Takes a snapshot of the canvas to create a GIF."""
        buf = BytesIO()
        fig.savefig(
            buf,
            format="png",
            bbox_inches="tight",
            pad_inches=self._pad,
            facecolor=self._facecolor,
        )
        buf.seek(0)
        img = imageio.imread(buf)
        self._frames.append(img)
        buf.close()
        plt.close(fig)
        
    def _save(self):
        """Save the collected frames as a GIF (uniform shape)."""
        if not self._frames:
            raise ValueError("No frames captured to save.")
            
        output_fp = Path(self._path)
        output_fp.parent.mkdir(parents=True, exist_ok=True)
        
        # Match all frames to smallest common shape
        min_h = min(f.shape[0] for f in self._frames)
        min_w = min(f.shape[1] for f in self._frames)
        resized_frames = [f[:min_h, :min_w, ...] for f in self._frames]
        
        # loop=0 means infinite loop, loop=1 means play once
        imageio.mimsave(self._path, resized_frames, fps=self._fps, loop=0 if self._loop else 1)
        self._saved = True
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        
        self._save()
        with open(self._path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode("utf-8")
        
        # Create HTML img tag — nbconvert captures this correctly
        html = f'<img src="data:image/gif;base64,{b64}" loop="infinite" />'
        
        # Display works both in live notebook and in exported HTML
        display(HTML(html))