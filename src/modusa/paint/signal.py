import numpy as np

def signal(
    ax,
    y,
    x=None,
    c=None,
    ls=None,
    lw=None,
    m=None,
    ms=3,
    legend=None
    ):
    """
    Plot a 1D signal on the given Matplotlib axis.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Matplotlib axis on which to draw the signal.
    y : np.ndarray
        The signal values to be plotted on the y-axis.
    x : np.ndarray, optional
        The corresponding x-axis values. If not provided, the function 
        uses the indices of `y` (i.e., `np.arange(len(y))`).
    c : str, optional
        Line color (e.g., 'r', 'blue', '#1f77b4'). Defaults to Matplotlib’s
        automatic color cycle.
    ls : str, optional
        Line style (e.g., '-', '--', '-.', ':'). Defaults to a solid line.
    lw : float, optional
        Line width in points. Defaults to Matplotlib’s default line width.
    m : str, optional
        Marker style (e.g., 'o', 'x', '^', '.'). No marker is drawn if None.
    ms : float, default=3
        Marker size in points.
    legend : str, optional
        Label for the signal. If provided, the function adds a legend entry.

    Returns
    -------
    None
        This function modifies the provided axis in-place.

    Notes
    -----
    - This function is a convenience wrapper for `ax.plot()`.
    """
        
    if x is None: x = np.arange(y.size)
        
    ax.plot(x, y, color=c, linestyle=ls, linewidth=lw, marker=m, markersize=ms, label=legend)
