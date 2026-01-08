def events(
    ax,
    xs,
    y0=None,
    y1=None,
    c=None,
    ls="-",
    lw=None,
    label=None,
):
    """
    Draw vertical lines (event markers) on the given Matplotlib axis.

    Typically used to visualize discrete events such as onsets, beats,
    or boundaries within a time series or spectrogram.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Matplotlib axis on which to draw the vertical lines.
    xs : array_like
        Sequence of x-values where vertical lines will be drawn.
    y0 : float or array_like, optional
        The starting y-coordinate(s) for the lines. Defaults to the bottom
        of the current y-axis limit if None.
    y1 : float or array_like, optional
        The ending y-coordinate(s) for the lines. Defaults to the top
        of the current y-axis limit if None.
    c : str, optional
        Color of the vertical lines (e.g., 'k', 'red', '#1f77b4').
        Defaults to Matplotlib’s automatic color cycle.
    ls : str, default='-'
        Line style (e.g., '-', '--', '-.', ':').
    lw : float, optional
        Line width in points. Defaults to Matplotlib’s default line width.
    label : str, optional
        Label for the line(s). Used for legends if provided.

    Returns
    -------
    None
        This function modifies the provided axis in-place.

    Notes
    -----
    - This is a convenience wrapper for `ax.vlines()`.
    - If multiple `xs` values are provided, a line is drawn for each.
    - Commonly used to mark temporal events like onsets in visualizations.
    """
        
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    
    if y0 is None: y0 = ylim[0]
    if y1 is None: y1 = ylim[1]
    
    for i, x in enumerate(xs):
        if xlim is not None:
            if xlim[0] <= x <= xlim[1]:
                if i == 0:  # Label should be set only once for all the events
                    ax.vlines(x, y0, y1, color=c, linestyle=ls, linewidth=lw, label=label)
                else:
                    ax.vlines(x, y0, y1, color=c, linestyle=ls, linewidth=lw)
        else:
            if i == 0:  # Label should be set only once for all the events
                ax.vlines(x, y0, y1, color=c, linestyle=ls, linewidth=lw, label=label)
            else:
                ax.vlines(x, y0, y1, color=c, linestyle=ls, linewidth=lw)
