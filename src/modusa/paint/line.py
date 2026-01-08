def line(ax, start, end, c="black", ls="-", lw=1.5, label=None, z=5):
    x_values = [start[0], end[0]]
    y_values = [start[1], end[1]]
    
    ax.plot(
        x_values,
        y_values,
        color=c,
        linestyle=ls,
        linewidth=lw,
        label=label,
        zorder=z,
    )
