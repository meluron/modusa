def ticks(
    ax,
    yticks=None,
    yticklabels=None,
    xticks=None,
    xticklabels=None,
):
    """
    Set tick positions and tick labels for a given axis.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axis on which tick settings will be applied.
    yticks : sequence of float, optional
        Tick positions for the y-axis.
    yticklabels : sequence of str, optional
        Tick labels corresponding to `yticks`. Length must match `yticks`. Default is None.
    xticks : sequence of float, optional
        Tick positions for the x-axis. Default is None.
    xticklabels : sequence of str, optional
        Tick labels corresponding to `xticks`. Default is None.

    Returns
    -------
    None
    """
    
    if yticks is not None:
        ax.set_yticks(yticks)
    if yticklabels is not None:
        ax.set_yticklabels(yticklabels)
    if xticks is not None:
        ax.set_xticks(xticks)
    if xticklabels is not None:
        ax.set_xtickslabels(xticklabels)
