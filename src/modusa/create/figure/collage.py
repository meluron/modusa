import modusa as ms
from ._sharedutils import generate_abc, load_devanagari_font

import matplotlib.pyplot as plt
import numpy as np

def collage(
    config,
    size=3,
    hspace_inches=1.0,
    wspace_inches=1.0,
    ylims=None,
    xlims=None,
    ylabels=None,
    xlabels=None,
    titles=None,
    grid=True,
    remove_ticks=False,
    abc=True,
    fig_num=""
):
    """
    Generate a 2D grid-style figure layout (collage) for displaying multiple subplots.

    This function creates a uniform grid of subplots (rows × columns) for visualizing
    multiple plots side by side in a consistent layout. It supports per-subplot customization
    for axis limits, labels, and titles, along with options for grids, tick removal, and
    alphabetical subplot tagging for research-style figures.

    Parameters
    ----------
    config : tuple[int, int]
        Grid configuration in the form `(n_rows, n_cols)`.
    size : float, default=3
        Size (in inches) of each grid cell along one dimension.
        The total figure size will be approximately `(size * n_cols, size * n_rows)`.
    hspace_inches : float, default=0.4
        Vertical gap between subplot rows (in inches).
    wspace_inches : float, default=0.4
        Horizontal gap between subplot columns (in inches).        
    ylims : list[tuple[float, float]] or None, optional
        A list of (min, max) pairs specifying y-axis limits for each subplot.
        Length must match the total number of subplots if provided.
    xlims : list[tuple[float, float]] or None, optional
        A list of (min, max) pairs specifying x-axis limits for each subplot.
        Length must match the total number of subplots if provided.
    ylabels : list[str] or None, optional
        A list of y-axis labels for each subplot.
    xlabels : list[str] or None, optional
        A list of x-axis labels for each subplot.
    titles : list[str] or None, optional
        A list of titles for each subplot.
    grid : bool, default=True
        Whether to display gridlines in each subplot.
    remove_ticks : bool, default=False
        Whether to remove x and y ticks from all subplots.
    abc : bool, default=True
        Whether to label each subplot with a small reference tag (e.g., "(a)", "(b)", "(c)")
        for research paper–style referencing.
    fig_num : str or int or float, default=""
        Optional prefix to the alphabetical subplot labels, e.g. "1a", "2b", etc.
    
    Returns
    -------
    fig : matplotlib.figure.Figure
        The created Matplotlib Figure object.
    axs : numpy.ndarray of matplotlib.axes.Axes
        A 2D array of Axes objects with shape `(n_rows, n_cols)` representing the subplot grid.
    """

    load_devanagari_font()
    
    n_rows, n_cols = config

    # Each cell = `size` height; total vertical spacing = (n_rows - 1) * hspace_inches
    fig_height = n_rows * size + (n_rows - 1) * hspace_inches
    fig_width = n_cols * size + (n_cols - 1) * wspace_inches

    # Convert absolute inches to relative normalized spacing
    avg_subplot_height = size
    avg_subplot_width = size
    hspace = hspace_inches / avg_subplot_height
    wspace = wspace_inches / avg_subplot_width

    # Create the grid
    fig, axs = plt.subplots(
        n_rows,
        n_cols,
        figsize=(fig_width, fig_height),
        gridspec_kw={"hspace": hspace, "wspace": wspace}
    )

    axs = np.atleast_2d(axs)
    axs_flat = axs.ravel()

    # --- Same configuration logic as before ---
    if abc:
        abc_labels = generate_abc(axs_flat.size)
        for i, ax in enumerate(axs_flat):
            ax.set_title(f"({fig_num}{abc_labels[i]})", fontsize=10, loc="left")

    if ylims is not None:
        for ylim, ax in zip(ylims, axs_flat):
            ms.set.view.limit(ax, ylim=ylim)
    if xlims is not None:
        for xlim, ax in zip(xlims, axs_flat):
            ms.set.limit(ax, xlim=xlim)
    if ylabels is not None:
        for ylabel, ax in zip(ylabels, axs_flat):
            ms.set.label(ax, ylabel=ylabel)
    if xlabels is not None:
        for xlabel, ax in zip(xlabels, axs_flat):
            ms.set.label(ax, xlabel=xlabel)
    if titles is not None:
        for title, ax in zip(titles, axs_flat):
            ms.set.title(ax, title=title)

    if grid:
        for ax in axs_flat:
            ms.set.view.gridlines(ax, x=True, y=True)
    if remove_ticks:
        for ax in axs_flat:
            ms.set.view.ticks(ax, left=False, bottom=False)

    return fig, axs
