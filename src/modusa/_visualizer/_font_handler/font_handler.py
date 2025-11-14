#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 09/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import matplotlib.font_manager as fm
import matplotlib as mpl
from pathlib import Path

def load_devanagari_font():
    """
    Load devanagari font as it works for Hindi labels.
    """
    
    # Path to your bundled font
    font_path = (Path(__file__).resolve().parents[0] / "fonts" / "NotoSansDevanagari-Regular.ttf")
    
    # Register the font with matplotlib
    fm.fontManager.addfont(str(font_path))
    
    # Get the font family name from the file
    hindi_font = fm.FontProperties(fname=str(font_path))
    
    # Set as default rcParam
    mpl.rcParams["font.family"] = [hindi_font.get_name(),"DejaVu Sans",]  # Fallback to DejaVu Sans
    