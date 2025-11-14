#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 09/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import matplotlib.pyplot as plt
from IPython import get_ipython

class Interactor:
    """
    Context manager to enable and manage interactive Matplotlib sessions in Jupyter.

    Usage:
        with Interactor() as interact:
            fig, ax = plt.subplots()
            interact.annotate(fig, ax)
    """

    def __init__(self):
        self.active = False
        self._ip = None

    def __enter__(self):
        self._ip = get_ipython()
        self._turn_on_interactive_mode()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._turn_off_interactive_mode()

    def _turn_on_interactive_mode(self):
        """Enable `%matplotlib widget` if possible."""
        plt.close("all")  # optional: cleans up old widget sessions

        if self._ip is None:
            print("⚠️ Not running inside IPython or Jupyter — interactive mode unavailable.")
            self.active = False
            return

        try:
            self._ip.run_line_magic("matplotlib", "widget")
            self.active = True
            print("✅ Interactive mode enabled (`%matplotlib widget`).")
        except Exception as e:
            print(f"⚠️ Could not enable interactive mode: {e}")
            print("Falling back to non-interactive backend.")
            self.active = False

    def _turn_off_interactive_mode(self):
        """Switch back to inline backend, but don't close the figure."""
        if self._ip is not None and self.active:
            try:
                self._ip.run_line_magic("matplotlib", "inline")
            except Exception:
                print("⚠️ Could not disable interactive mode cleanly.")
                
        
        self.active = False

    def annotate(self, fig, axs):
        """Wrapper for your annotator function."""
        from ._annotator import annotate
        if not self.active:
            print("⚠️ Interactive backend not active — annotations won't be interactive.")
        return annotate(fig, axs)


        
#def annotate(fig, axs):
#   
#   from ._annotator import annotate
#   
#   annotation: list[tuple[float, float, str]] | None = None
#   
#   try:
#       annotation = annotate(fig, axs)
#   except Exception as e:
#       import traceback
#       print("⚠️ Interactive mode needs to be turned on to annotate the figure. Please run the following before creating the figure:")
#       print('ms.interactive_mode("on")')
#   
#   return annotation