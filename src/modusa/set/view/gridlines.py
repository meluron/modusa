def gridlines(ax, x=True, y=True):
    """Add gridlines to the given axis."""
    ax.grid(which='major', axis=('x' if x and not y else 'y' if y and not x else 'both'),
            linestyle='--', linewidth=0.6, alpha=0.6)
    ax.minorticks_on() # Add minor ticks without tick labels.
