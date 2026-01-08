def limit(
    ax,
    ylim=None,
    xlim=None,
):
    """
    Set limits for a given axis.

    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axis to apply limits settings on.
    ylim: tuple[float, float], optional
        Limits to y-axis. Default is None.
    xlim: tuple[float, float], optional
        Limits to x-axis. Default is None.
    """
    if ylim is not None: ax.set_ylim(ylim)
    if xlim is not None: ax.set_xlim(xlim)
