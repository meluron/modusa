#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 09/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from collections.abc import Iterable

import fnmatch

class Painter:
    """
    
    """
        
    @staticmethod
    def signal(
    ax,
    y,
    x=None,
    c=None,
    ls=None,
    lw=None,
    m=None,
    ms=3,
    legend=None
    ):
        """
        Plot a 1D signal on the given Matplotlib axis.
    
        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The Matplotlib axis on which to draw the signal.
        y : np.ndarray
            The signal values to be plotted on the y-axis.
        x : np.ndarray, optional
            The corresponding x-axis values. If not provided, the function 
            uses the indices of `y` (i.e., `np.arange(len(y))`).
        c : str, optional
            Line color (e.g., 'r', 'blue', '#1f77b4'). Defaults to Matplotlib’s
            automatic color cycle.
        ls : str, optional
            Line style (e.g., '-', '--', '-.', ':'). Defaults to a solid line.
        lw : float, optional
            Line width in points. Defaults to Matplotlib’s default line width.
        m : str, optional
            Marker style (e.g., 'o', 'x', '^', '.'). No marker is drawn if None.
        ms : float, default=3
            Marker size in points.
        legend : str, optional
            Label for the signal. If provided, the function adds a legend entry.
    
        Returns
        -------
        None
            This function modifies the provided axis in-place.
    
        Notes
        -----
        - This function is a convenience wrapper for `ax.plot()`.
        """
            
        if x is None: x = np.arange(y.size)
            
        ax.plot(x, y, color=c, linestyle=ls, linewidth=lw, marker=m, markersize=ms, label=legend)
        
    @staticmethod
    def image(
        ax,
        M,
        y=None,
        x=None,
        c="gray_r",
        o="upper",
        clabel=None,
        cax=None,
        alpha=1,
    ):
        """
        Display a 2D or 3D image (e.g., grayscale or RGB) on the given Matplotlib axis.
    
        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The Matplotlib axis on which to render the image.
        M : np.ndarray
            The image or matrix to display. Can be:
                - 2D array for grayscale or matrix data.
                - 3D array (H, W, 3) for RGB images.
        y : np.ndarray, optional
            Values corresponding to the y-axis. If None, the image indices are used.
        x : np.ndarray, optional
            Values corresponding to the x-axis. If None, the image indices are used.
        c : str, default='gray_r'
            Colormap name used when `M` is a 2D array (e.g., 'viridis', 'gray').
            Ignored if `M` is RGB.
        o : {'upper', 'lower'}, default='upper'
            Origin of the image. 'upper' places [0, 0] at the top-left corner,
            while 'lower' places it at the bottom-left.
        clabel : str, optional
            Label for the colorbar. Displayed only if a colorbar is added.
        cax : matplotlib.axes.Axes, optional
            The axis on which to draw the colorbar. If None, no colorbar is drawn.
        alpha : float, default=1
            Opacity of the image. Must be between 0 (transparent) and 1 (opaque).
    
        Returns
        -------
        None
            This function modifies the provided axis in-place.
    
        Notes
        -----
        - This is a convenience wrapper for `ax.imshow()`.
        - If `M` is a 2D matrix and `cax` is provided, a colorbar is automatically added.
        """
    
        if x is None: x = np.arange(M.shape[1])
        if y is None: y = np.arange(M.shape[0])
            
        def _calculate_extent(x, y, o):
            """
            Calculate x and y axis extent for the
            2D matrix.
            """
            # Handle spacing safely
            if len(x) > 1:
                dx = x[1] - x[0]
            else:
                dx = 1  # Default spacing for single value
            if len(y) > 1:
                dy = y[1] - y[0]
            else:
                dy = 1  # Default spacing for single value
                
            if o == "lower":
                return [x[0] - dx / 2, x[-1] + dx / 2, y[0] - dy / 2, y[-1] + dy / 2]
            else:
                return [x[0] - dx / 2, x[-1] + dx / 2, y[-1] + dy / 2, y[0] - dy / 2]
            
        extent = _calculate_extent(x, y, o)
        
        im = ax.imshow(M, aspect="auto", origin=o, cmap=c, extent=extent, alpha=alpha)
                
        # Colorbar
        if cax is not None:
            cax.axis("on")
            cbar = plt.colorbar(im, cax=cax)
            if clabel is not None:
                cbar.set_label(clabel, labelpad=5)
                
            
    @staticmethod
    def annotation(
        ax,
        ann,
        text_loc="m",
        alpha=0.7,
    ):
        """
        Draw annotation spans on the given Matplotlib axis.
    
        Typically used to visualize labeled regions or time spans (e.g., phoneme or word
        boundaries) produced by `modusa.load.annotation()`.
    
        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The Matplotlib axis on which to draw the annotations.
        ann : list of tuple
            List of annotation spans. Each tuple should have the form:
            `(start, end, label, confidence, group)` where:
                - `start` (float): Start position (e.g., in seconds or samples).
                - `end` (float): End position.
                - `label` (str): Annotation label.
                - `confidence` (float or None): Incase CTM gives confidence values.
                - `group` (int or None): Incase you grouped together different labels.
        text_loc : {'b', 'm', 't'}, default='m'
            Vertical position of the text label within each annotation box:
                - `'b'` → bottom
                - `'m'` → middle
                - `'t'` → top
        alpha : float, default=0.7
            Transparency level of the annotation boxes.
            Must be between 0 (fully transparent) and 1 (fully opaque).
    
        Returns
        -------
        None
            This function modifies the provided axis in-place.
    
        Notes
        -----
        - Each annotation span is rendered as a colored rectangle with an optional text label.
        - The color of each rectangle is determined internally based on the group.
        - Useful for visualizing segment boundaries in time-aligned data such as audio,
            or event sequences.
        """

        
        # Get the xlim as we will only be plotting for the region defined by xlim
        xlim: tuple[float, float] = ax.get_xlim()
        ylim: tuple[float, float] = ax.get_ylim()
                
        colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
        
        # Text Location
        if text_loc in ["b", "bottom", "lower", "l"]:
            text_yloc = ylim[0] + 0.1 * (ylim[1] - ylim[0])
        elif text_loc in ["t", "top", "u", "upper"]:
            text_yloc = ylim[1] - 0.1 * (ylim[1] - ylim[0])
        else:
            text_yloc = (ylim[1] + ylim[0]) / 2
            
        for i, (start, end, label, confidence, group) in enumerate(ann):
            # We make sure that we only plot annotation that are within the x range of the current view
            if xlim is not None:
                if start >= xlim[1] or end <= xlim[0]:
                    continue
                
                # Clip boundaries to xlim
                start = max(start, xlim[0])
                end = min(end, xlim[1])
                
                if group is not None:
                    box_color = colors[group]
                else:
                    box_color = "lightgray"
                    
                width = end - start
                rect = Rectangle((start, ylim[0]), width, ylim[1] - ylim[0], facecolor=box_color, edgecolor="black", alpha=alpha)
                ax.add_patch(rect)
                
                text_obj = ax.text((start + end) / 2, text_yloc, label, ha="center", va="center", fontsize=12, color="black", zorder=10, clip_on=True)
                
                text_obj.set_clip_path(rect)
            else:
                if group is not None:
                    box_color = colors[group]
                else:
                    box_color = "lightgray"
                    
                width = end - start
                rect = Rectangle((start, ylim[0]), width, ylim[1] - ylim[0], facecolor=box_color, edgecolor="black", alpha=alpha)
                ax.add_patch(rect)
                
                text_obj = ax.text((start + end) / 2, text_yloc, label, ha="center", va="center", fontsize=12, color="black", zorder=10, clip_on=True)
                
                text_obj.set_clip_path(rect)

            
    @staticmethod
    def vlines(
        ax,
        xs,
        y0=None,
        y1=None,
        c=None,
        ls="-",
        lw=None,
        label=None,
    ):
        """
        Draw vertical lines (event markers) on the given Matplotlib axis.
    
        Typically used to visualize discrete events such as onsets, beats,
        or boundaries within a time series or spectrogram.
    
        Parameters
        ----------
        ax : matplotlib.axes.Axes
            The Matplotlib axis on which to draw the vertical lines.
        xs : array_like
            Sequence of x-values where vertical lines will be drawn.
        y0 : float or array_like, optional
            The starting y-coordinate(s) for the lines. Defaults to the bottom
            of the current y-axis limit if None.
        y1 : float or array_like, optional
            The ending y-coordinate(s) for the lines. Defaults to the top
            of the current y-axis limit if None.
        c : str, optional
            Color of the vertical lines (e.g., 'k', 'red', '#1f77b4').
            Defaults to Matplotlib’s automatic color cycle.
        ls : str, default='-'
            Line style (e.g., '-', '--', '-.', ':').
        lw : float, optional
            Line width in points. Defaults to Matplotlib’s default line width.
        label : str, optional
            Label for the line(s). Used for legends if provided.
    
        Returns
        -------
        None
            This function modifies the provided axis in-place.
    
        Notes
        -----
        - This is a convenience wrapper for `ax.vlines()`.
        - If multiple `xs` values are provided, a line is drawn for each.
        - Commonly used to mark temporal events like onsets in visualizations.
        """
            
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        if y0 is None: y0 = ylim[0]
        if y1 is None: y1 = ylim[1]
        
        for i, x in enumerate(xs):
            if xlim is not None:
                if xlim[0] <= x <= xlim[1]:
                    if i == 0:  # Label should be set only once for all the events
                        ax.vlines(x, y0, y1, color=c, linestyle=ls, linewidth=lw, label=label)
                    else:
                        ax.vlines(x, y0, y1, color=c, linestyle=ls, linewidth=lw)
            else:
                if i == 0:  # Label should be set only once for all the events
                    ax.vlines(x, y0, y1, color=c, linestyle=ls, linewidth=lw, label=label)
                else:
                    ax.vlines(x, y0, y1, color=c, linestyle=ls, linewidth=lw)
    
    @staticmethod
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
    
    @staticmethod
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



    @staticmethod
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
