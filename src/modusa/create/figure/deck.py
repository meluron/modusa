import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.lines as mlines
import numpy as np
from ._sharedutils import load_devanagari_font

def deck(config, tile_size=1, overlap=0.3, focus=None, focus_offset=2.0):
    """
    Generate 3D stacks like canvas based on the configuration.

    Testing Phase. Not yet allowed for user to access it.
    """

    load_devanagari_font()
    
    fig = plt.figure(figsize=(tile_size * 2, tile_size * 2))
    axs = []

    width, height = 0.8, 0.8
    base_positions = [(0.1 + i * overlap * 0.1, 0.1 + i * overlap * 0.1) for i in range(config)]

    for i in range(config):
        left, bottom = base_positions[i]
        ax = fig.add_axes([left, bottom, width, height], facecolor="white", zorder=(config - i))
        ax.patch.set_edgecolor("black")
        ax.patch.set_linewidth(1.5)

        # FIX 1: lock aspect ratio and prevent auto-scaling
        ax.set_aspect("equal", adjustable="box")
        ax.set_autoscale_on(False)
        ax.autoscale(False)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        axs.append(ax)

    # FIX 2: Hide ticks consistently
    for i, ax in enumerate(axs):
        if not (focus is not None and i == focus):
            ax.set_xticks([])
            ax.set_yticks([])

    # Handle focus highlight
    if focus is not None and 0 <= focus < config:
        left, bottom = base_positions[focus]
        new_left = left + focus_offset
        new_bottom = bottom

        ghost_rect = Rectangle(
            (left, bottom),
            width, height,
            transform=fig.transFigure,
            facecolor="gray",
            edgecolor="red",
            linewidth=1.0,
            linestyle="-",
            zorder=(config - focus) - 0.5,
        )
        fig.patches.append(ghost_rect)

        x0 = left + width
        y0 = bottom + height * 0.5
        x1 = new_left
        y1 = new_bottom + height * 0.5

        connector = mlines.Line2D(
            [x0, x1],
            [y0, y1],
            transform=fig.transFigure,
            linestyle="--",
            linewidth=1.0,
            color="red",
            zorder=(config - focus) - 0.5,
        )
        fig.lines.append(connector)

        axs[focus].set_position([new_left, new_bottom, width, height])
        axs[focus].patch.set_edgecolor("red")
        axs[focus].patch.set_linewidth(2.5)
        axs[focus].set_zorder(config + 1)

    return fig, np.array(axs)
