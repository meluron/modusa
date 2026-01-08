import numpy as np

def arrow(
        ax,
        start,
        end,
        c="black",
        head_size=0.02,
        head_label=None,
        tail_label=None,
        arrow_label=None,
        offset=0.05,
    ):
        """
        Draw a labeled arrow from a start point to an end point with automatic label positioning.
    
        Useful for illustrating vectors, directions, or relationships between two points
        in a 2D coordinate space.
    
        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The Matplotlib axis on which to draw the arrow.
        start : tuple[float, float]
            Coordinates of the arrow's starting point `(x_start, y_start)`.
        end : tuple[float, float]
            Coordinates of the arrow's ending point `(x_end, y_end)`.
        c : str, default='black'
            Color of the arrow and its labels.
        head_size : float, default=0.05
            Relative size of the arrowhead. Larger values make the arrowhead more prominent.
        head_label : str, optional
            Optional text label displayed near the arrowhead.
        tail_label : str, optional
            Optional text label displayed near the tail (starting point).
        arrow_label : str, optional
            Optional text label displayed near the midpoint of the arrow.
        offset : float, default=0.05
            Offset distance (in data units) used to slightly displace text labels
            perpendicular to the arrow direction to prevent overlap.
    
        Returns
        -------
        None
            This function modifies the provided axis in-place.
    
        Notes
        -----
        - The arrow is drawn using `ax.annotate()` or `ax.arrow()` for flexibility and control.
        - Label placement is automatically adjusted to improve readability.
        - Can be combined with `ax.text()` or other annotations for more complex diagrams.

        """
        x_start, y_start = start
        x_end, y_end = end
        
        # Compute direction vector (for auto label offset)
        dx = x_end - x_start
        dy = y_end - y_start
        mag = np.hypot(dx, dy)
        if mag == 0:
            return  # skip zero-length arrow
        
        # Normalized direction and perpendicular vectors
        ux, uy = dx / mag, dy / mag
        px, py = -uy, ux  # perpendicular vector (for label offsets)
        # Offset magnitude in data units
        ox, oy = px * offset, py * offset
        
        # Draw arrow
        ax.annotate(
            "",
            xy=(x_end, y_end),
            xytext=(x_start, y_start),
            arrowprops=dict(
                arrowstyle=f"->,head_length={head_size*20},head_width={head_size*10}",
                color=c,
                lw=1.5,
            ),
        )
        
        # Draw points
        ax.scatter(*start, color=c, s=10, zorder=3)
        
        # Label start and end points
        text_offset = 10 # offset in display coordinates (pixels)
        
        if tail_label:
            ax.annotate(tail_label, xy=start, xycoords="data", xytext=(-ux * text_offset, -uy * text_offset), textcoords="offset points", ha="center", va="center", color=c, fontsize=10, arrowprops=None)
            
        if head_label:
            ax.annotate(head_label, xy=end, xycoords="data", xytext=(ux * text_offset, uy * text_offset), textcoords="offset points", ha="center", va="center", color=c, fontsize=10, arrowprops=None)
            
            # Label arrow at midpoint (also offset)
        if arrow_label:
            xm, ym = (x_start + x_end) / 2, (y_start + y_end) / 2
            ax.text(xm + ox, ym + oy, arrow_label, color=c, fontsize=10, ha="center")
