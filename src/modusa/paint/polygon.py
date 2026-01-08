import numpy as np

def polygon(
    ax,
    points,
    c=None,
    ec="black",
    alpha=0.5,
    lw=1.0,
    fill=True,
):
    """
    Draw a polygon defined by a sequence of 2D vertices on the given Matplotlib axis.

    Useful for visualizing areas, regions of interest, or geometric shapes
    within a 2D coordinate space.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        The Matplotlib axis on which to draw the polygon.
    points : np.ndarray of shape (n_points, 2)
        Array of 2D coordinates representing vertices of the polygon in order.
        The polygon is automatically closed between the last and first points.
    c : str, optional
        Fill color for the polygon. If None, a default color (e.g., Matplotlib’s
        auto color cycle) is used.
    ec : str, default='black'
        Edge color for the polygon boundary.
    alpha : float, default=0.5
        Transparency level of the fill (0 = fully transparent, 1 = fully opaque).
    lw : float, default=1.0
        Line width of the polygon edges.
    fill : bool, default=True
        Whether to fill the polygon with color. If False, only the outline is drawn.

    Returns
    -------
    None
        This function modifies the provided axis in-place.

    Notes
    -----
    - This function is a wrapper around `matplotlib.patches.Polygon`.
    - Use `ax.add_patch()` to manually add or customize the returned polygon if needed.
    - The polygon is automatically closed.
    """
    points = np.asarray(points)
    
    # Close the polygon if not already closed
    if not np.all(points[0] == points[-1]):
        points = np.vstack([points, points[0]])
        
    if fill:
        ax.fill(points[:, 0], points[:, 1], color=c, alpha=alpha, edgecolor=ec, linewidth=lw)
    else:
        ax.plot(points[:, 0], points[:, 1], color=ec, linewidth=lw)
