def legend(ax):
    """
    Add legend to a given axis.

    Parameters
    ----------
    ax: matplotlib.axes.Axes
        Axis to show legend for.

    Returns
    -------
    None
    """
    
    # --- Individual legends per subplot ---
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(handles, labels, loc="upper right", frameon=True)
