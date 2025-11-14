Visualizer
==========

The visualizer module helps you present your data clearly and consistently.
It provides a simple, three-step workflow for creating visual layouts:

1. **Select a figure layout**: Choose from preset layouts such as tiers, grids, stacks, or cartesian.
2. **Configure it**: Adjust parameters like size, overlap, and axis limits.
3. **Paint the figure**: Use the painter API to draw signals, annotations, and other elements.

Figure Layouts
^^^^^^^^^^^^^^

The following layout presets are available:

.. automethod:: modusa.figlayouts.tracks
.. automethod:: modusa.figlayouts.collage
.. automethod:: modusa.figlayouts.deck

----

Painter
^^^^^^^
This class is not intended to be used directly. The `canvas` class object has a `paint` property that returns an instance of this calls which various APIs to paint the canvas. Below is how it is supposed to be used.

.. automethod:: modusa.paint.signal
.. automethod:: modusa.paint.image
.. automethod:: modusa.paint.annotation
.. automethod:: modusa.paint.vlines
.. automethod:: modusa.paint.arrow

----

Animator
^^^^^^^^

`Animator` is a context-managed animation builder designed to capture a sequence of frames
from `Canvas` objects and save them as a GIF. It can automatically display the resulting GIF
in Jupyter notebooks and in exported HTML.

.. code-block:: python
    
    import numpy as np
    import modusa as ms
    
    X = np.random.random((5, 10, 5))
    with ms.animate("./wave.gif", fps=4, pad=0.4, loop=True) as anim:
        for frame in range(5):
            cnv = ms.canvas.stacks(5, focus=frame)
            for i in range(frame+1):
                cnv.paint.image(X[i,:,:])
            anim.snapshot(cnv)

----

Distribution Plot
^^^^^^^^^^^^^^^^^
The `modusa.hill_plot` function generates a distribution plot, typically used to visualize the statistical spread or density of a dataset. This is useful for understanding patterns, skewness, and overall behavior of your data.

.. autofunction:: modusa.hill_plot

----