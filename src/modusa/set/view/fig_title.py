def fig_title(
    fig,
    title=None,
    c="red",
    s=12,
    y=1.0
):
    """
    Set the title for the figure.

    Parameters
    ----------
    fig: matplotlib.Figure
        Figure to add title to.
    title: str, optional
        Title for the figure. Default is None.
    c: str, optional
        Color of the title text. Default is "red".
    s: int, optional
        Size of the title text. Default is 10.
    y: float, optional
        y-position for the title placement. Default is 1.0.

    Returns
    -------
    None
    """
    
    if title is not None:
        fig.suptitle(title, size=s, y=y, color=c)
