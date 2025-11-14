#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 09/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.lines as mlines
import numpy as np
import string

# Load Devanagari font
from .._font_handler.font_handler import load_devanagari_font
load_devanagari_font()

from .._style_setter.style_setter import StyleSetter as set

class FigLayoutGenerator:
    
    def _generate_abc(n):
        """
        Generate lowercase labels: a, b, ..., z, aa, ab, ac, ...
        for tiles/axs.
        """
        labels = []
        letters = string.ascii_lowercase
        while len(labels) < n:
            i = len(labels)
            label = ""
            while True:
                label = letters[i % 26] + label
                i = i // 26 - 1
                if i < 0:
                    break
            labels.append(label)
        return labels
    
    @staticmethod
    def tracks(
        config,
        ylims=None,
        xlim=None,
        ylabels=None,
        xlabels=None,
        titles=None,
        grid=True,
        fig_width=18,
        hspace_inches=0.4,
        abc=True,
        fig_num="",
        
    ):
        """
        Create a Praat-style multi-track figure layout where all tracks share the same x-axis 
        (typically representing time), with consistent physical heights and uniform spacing 
        between tracks.
    
        This method provides a flexible and publication-ready layout generator for 
        time-aligned visualizations such as signals, annotations, and spectrograms.
    
        Parameters
        ----------
        config : str
            A string specifying the types and order of tracks to display.
            Each character represents one track:
            - "a": auxiliary track (e.g., annotation, pitch, energy, etc.)
            - "s": signal track (e.g., waveform)
            - "m": matrix track (e.g., spectrogram, feature matrix)
            Example:
                "asm" → one auxiliary track, one signal track, one matrix track.
        ylims : list[tuple[float, float]] or None, optional
            A list of (min, max) pairs specifying y-axis limits for each track.
            Length must match the number of tracks if provided.
        xlim : tuple[float, float] or None, optional
            The x-axis limit shared across all tracks.
        ylabels : list[str] or None, optional
            A list of y-axis labels for each track.
        xlabels : list[str] or None, optional
            A list of x-axis labels for each track.
        titles : list[str] or None, optional
            A list of titles for each track.
        grid: bool, default=True
            Adds gridlines to the tracks.
        fig_width : float, default=18
            Total figure width (in inches).
        hspace_inches : float, default=0.4
            Vertical gap (in inches) between consecutive tracks.
            This is converted internally to a relative spacing value to preserve
            exact physical spacing across configurations.
        abc : bool, default=True
            Whether to label each subplot with a small reference tag (e.g., "(a)", "(b)", "(c)")
            for research paper style referencing.
        fig_num : str or int or float, default=""
            Optional prefix to the alphabetical subplot labels, e.g. "1a", "2b", etc.
        
        Returns
        -------
        fig : matplotlib.figure.Figure
            The created Matplotlib Figure object.
        axs : numpy.ndarray of matplotlib.axes.Axes
            A 2D array of Axes objects of shape (n_tracks, 2), where column 0 contains
            the actual tracks and column 1 is reserved for colorbars (for matrix plots).
        """
        
        # Setup the variables
        tracks = config
        
        # Parse the config
        n_aux_tracks = config.count("a")
        n_signal_tracks = config.count("s")
        n_matrix_tracks = config.count("m")
        n_tracks = n_aux_tracks + n_signal_tracks + n_matrix_tracks  # Number of tracks
        
        # Decide heights of different tracks type
        height = {}
        height["a"] = 0.4  # Aux height
        height["s"] = 2.0  # Signal height
        height["m"] = 4.0  # Matrix height
        cbar_width = 0.01  # For second column (for matrix track)
        
        # Calculate height ratios for each track
        height_ratios = [height[track] for track in tracks]
            
        # Calculate total fig height
        fig_height = np.sum(height_ratios) + (len(tracks) - 1) * hspace_inches
        
        # Compute hspace wrt the average subplot heights (matplot uses this)
        total_subplot_height = sum(height_ratios)
        avg_subplot_height = total_subplot_height / len(tracks)
        hspace = hspace_inches / avg_subplot_height
        
        # Generate the layout
        fig, axs = plt.subplots(n_tracks, 2, figsize=(fig_width, fig_height), gridspec_kw={"height_ratios": height_ratios, "width_ratios": [1, cbar_width], "hspace": hspace})
        
        axs = np.atleast_2d(axs)  # This is done for consistency otherwise axs[i, 0] does not work

        for i, track in enumerate(tracks):  # Loop through each tier and adjust the layout
            if track == "a":  # Remove ticks and labels from all the aux subplots
                axs[i, 0].tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
            elif track == "s":
                axs[i, 0].tick_params(bottom=False, labelbottom=False)
            elif track == "m":
                axs[i, 0].tick_params(bottom=False, labelbottom=False)
            
            axs[i, 1].axis("off")  # Turn off the column 2, only turn it on when matrix is plotted with colorbar
            
            axs[i, 0].sharex(axs[0, 0])  # Share the x-axis to make all the tiers aligned
        
        # Add tags (1a, 4.1c, ...) to each tier for better referencing in research papers.
        if abc is True:
            abc_labels = FigLayoutGenerator._generate_abc(n_tracks)
            for i in range(n_tracks):
                axs[i, 0].set_title(f"({fig_num}{abc_labels[i]})", fontsize=10, loc="left")
                
        # Turn on the x-label for the last tier
        axs[-1, 0].tick_params(bottom=True, labelbottom=True)
        
        # Configure the styling
        if ylims is not None:
            for (ylim, ax) in zip(ylims, axs[:,0]):
                set.limit(ax, ylim=ylim)
        if xlim is not None:
            set.limit(axs[0,0], xlim=xlim)
        if ylabels is not None:
            for (ylabel, ax) in zip(ylabels, axs[:,0]):
                set.label(ax, ylabel=ylabel)
        if xlabels is not None:
            for (xlabel, ax) in zip(xlabels, axs[:,0]):
                set.label(ax, xlabel=xlabel)
        if titles is not None:
            for (title, ax) in zip(titles, axs[:,0]):
                set.title(ax, title=title)
        if grid is True:
            for ax in axs[:,0]:
                set.gridlines(ax, x=True, y=True)
            
        return fig, axs
    
    
    @staticmethod
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
            abc_labels = FigLayoutGenerator._generate_abc(axs_flat.size)
            for i, ax in enumerate(axs_flat):
                ax.set_title(f"({fig_num}{abc_labels[i]})", fontsize=10, loc="left")
    
        if ylims is not None:
            for ylim, ax in zip(ylims, axs_flat):
                set.limit(ax, ylim=ylim)
        if xlims is not None:
            for xlim, ax in zip(xlims, axs_flat):
                set.limit(ax, xlim=xlim)
        if ylabels is not None:
            for ylabel, ax in zip(ylabels, axs_flat):
                set.label(ax, ylabel=ylabel)
        if xlabels is not None:
            for xlabel, ax in zip(xlabels, axs_flat):
                set.label(ax, xlabel=xlabel)
        if titles is not None:
            for title, ax in zip(titles, axs_flat):
                set.title(ax, title=title)
    
        if grid:
            for ax in axs_flat:
                set.gridlines(ax, x=True, y=True)
        if remove_ticks:
            for ax in axs_flat:
                set.ticks(ax, left=False, bottom=False)
    
        return fig, axs
    
    @staticmethod
    def _deck(config, tile_size=1, overlap=0.3, focus=None, focus_offset=2.0):
        """
        Generate 3D stacks like canvas based on the configuration.

        Testing Phase. Not yet allowed for user to access it.
        """
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