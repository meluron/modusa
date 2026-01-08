def label(
    ax,
    ylabel=None,
    xlabel=None,
    c = "blue",
    s = 10
):
    """
    Set label for x and y axis.
    
    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axis to apply label settings on.
    ylabel: str, optional
        Label for y-axis. Default is None.
    xlabel: str, optional
        Label for x-axis. Default is None.
    c: str, optional
        Color of the label text. Default is "blue".
    s: int, optional
        Size of the label text. Default is 10.
    
    Returns
    -------
    None
    """
    if ylabel is not None:
        ax.set_ylabel(ylabel + "→", color=c, size=s)
    
    if xlabel is not None:
        ax.set_xlabel(xlabel + "→", color=c, size=s)
