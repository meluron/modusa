#============================================
# Modusa Models
#============================================
#-------- Annotation Model ---------
from ._models.annotation.annotation import Annotation as annotation

#-------- Audio Model ---------
from ._models.audio.audio import Audio as audio

#-------- Image Model ---------
from ._models.image.image import Image as image

#============================================
# Modusa Models Loader
#============================================
from ._loader.loader import Loader as load

# Synthesizer
from ._synthesizer.synthesizer import Synthesizer as synthesize

# Media Player
from ._mediaplayer.mediaplayer import MediaPlayer as play

# Media Recorder
from ._mediarecorder.mediarecorder import MediaRecorder as record

# Saver
from ._saver.saver import Saver as saveas

# Feature Extractor
from ._feature_extractor.feature_extractor import FeatureExtractor as extract

# =================== Visualizer ======================
# Figure Layout Generator
from ._visualizer._figlayout_generator.figlayout_generator import FigLayoutGenerator as figlayouts

# Painter
from ._visualizer._painter.painter import Painter as paint

# Style Setter
from ._visualizer._style_setter.style_setter import StyleSetter as set

# Interactor
from ._visualizer._interactor.interactor import Interactor as interact

# Animator
from ._visualizer._animator.animator import Animator as animate

# Quick Plotter
from ._visualizer._painter._quick_plotter import hill_plot
#==========================================================

# Tools
import modusa.tools

#====================
# RELEASE VERSION (MAJOR.MINOR.PATCH)

__version__ = "4.4.2" # This is dynamically used by the documentation, and pyproject.toml; Only need to change it here; rest gets taken care of.
#====================
