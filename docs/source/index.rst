modusa
======

``modusa`` is a Python library for streamlined **audio analysis** designed for musicians, researchers, and engineers working in **MIR** and **speech analysis**.

It offers purpose-built tools for the audio domain, combining **audio loading**, **annotation handling**, **visualization**, and **analysis** in a unified, easy-to-use API.  
``modusa`` simplifies common workflows so you can focus on **experimentation and insight**, not boilerplate code.

Key Features
------------

- **Flexible Audio Loader**  
   Load audio in multiple formats (``WAV``, ``MP3``, ``FLAC``, ``M4A``, ``AAC``, ``OPUS``, ``AIFF``) — even directly from YouTube links.
   
- **Unified Annotation Interface**  
   Work with ``.txt`` (Audacity labels) and ``.ctm`` (ASR/FA outputs) annotations seamlessly. ``TextGrid`` support coming soon.
   
- **Modular Plotter**  
   Create time-aligned visualizations combining waveforms, annotations, and spectrograms with minimal code.  
   Supports multi-tier figures, dark mode, legends, tier IDs, and grouped color patterns.
   
- **Interactive Audio Player**  
   Play audio with visible annotation labels directly inside notebooks.
   
- **Built-in Audio Recorder**  
   Capture and instantly analyze microphone input from within Jupyter.
   
- **Analytical Tools**  
   Includes quick plotting utilities like distribution (hill) plots for comparing numerical features.


.. toctree::
   :maxdepth: 1
   :caption: Quick Tour to Modusa
   
   How to use modusa? <https://meluron.github.io/devquest/htmls/MODUSA-%5B01%5D_A_Quick_Guide.html>
   quicktour/evolution
   
   

.. toctree::
   :maxdepth: 1
   :caption: API Reference
   
   tools/index
   


   
   
   

