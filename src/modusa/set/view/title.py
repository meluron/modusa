def title(
    ax,
    title=None,
    c="green",
    s=10,
):
    """
    Set title for a given axis.

    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axis to set title for.
    title: str, optional
        Title for the axis.
    c: str, optional
        Color of the title text. Default is "green".
    s: int, optional
        Size of the title text. Default is 10.
    """
    if title is not None:
        ax.set_title(title, size=s, loc="right", color=c)
