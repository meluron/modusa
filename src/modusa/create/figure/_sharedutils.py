import string
import matplotlib.font_manager as fm
import matplotlib as mpl
from pathlib import Path

def generate_abc(n):
    """
    Generate lowercase labels: a, b, ..., z, aa, ab, ac, ...
    for tiles/axs.
    """
    labels = []
    letters = string.ascii_lowercase
    while len(labels) < n:
        i = len(labels)
        label = ""
        while True:
            label = letters[i % 26] + label
            i = i // 26 - 1
            if i < 0:
                break
        labels.append(label)
    return labels


def load_devanagari_font():
    """
    Load devanagari font as it works for Hindi labels.
    """
    
    # Path to your bundled font
    font_path = (Path(__file__).resolve().parents[2] / "assets/fonts/NotoSansDevanagari-Regular.ttf")
    
    # Register the font with matplotlib
    fm.fontManager.addfont(str(font_path))
    
    # Get the font family name from the file
    hindi_font = fm.FontProperties(fname=str(font_path))
    
    # Set as default rcParam
    mpl.rcParams["font.family"] = [hindi_font.get_name(),"DejaVu Sans",]  # Fallback to DejaVu Sans
    