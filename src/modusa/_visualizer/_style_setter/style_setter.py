#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 09/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

import numpy as np
import matplotlib.pyplot as plt

class StyleSetter:
    """
    Utility class to apply style settings to matplotlib figure and axis.

    This class provides convenience methods to configure common styling
    parameters.
    """
    def __init__(self):
        pass
        
    @staticmethod
    def ticks(
        ax,
        yticks=None,
        yticklabels=None,
        xticks=None,
        xticklabels=None,
    ):
        """
        Set tick positions and tick labels for a given axis.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Axis on which tick settings will be applied.
        yticks : sequence of float, optional
            Tick positions for the y-axis.
        yticklabels : sequence of str, optional
            Tick labels corresponding to `yticks`. Length must match `yticks`. Default is None.
        xticks : sequence of float, optional
            Tick positions for the x-axis. Default is None.
        xticklabels : sequence of str, optional
            Tick labels corresponding to `xticks`. Default is None.

        Returns
        -------
        None
        """
        
        if yticks is not None:
            ax.set_yticks(yticks)
        if yticklabels is not None:
            ax.set_yticklabels(yticklabels)
        if xticks is not None:
            ax.set_xticks(xticks)
        if xticklabels is not None:
            ax.set_xtickslabels(xticklabels)


    @staticmethod
    def limit(
        ax,
        ylim=None,
        xlim=None,
    ):
        """
        Set limits for a given axis.

        Parameters
        ----------
        ax: matplotlib.axes.Axes
            Axis to apply limits settings on.
        ylim: tuple[float, float], optional
            Limits to y-axis. Default is None.
        xlim: tuple[float, float], optional
            Limits to x-axis. Default is None.
        """
        if ylim is not None: ax.set_ylim(ylim)
        if xlim is not None: ax.set_xlim(xlim)
    
    @staticmethod
    def label(
        ax,
        ylabel=None,
        xlabel=None,
        c = "blue",
        s = 10
    ):
        """
        Set label for x and y axis.
        
        Parameters
        ----------
        ax: matplotlib.axes.Axes
            Axis to apply label settings on.
        ylabel: str, optional
            Label for y-axis. Default is None.
        xlabel: str, optional
            Label for x-axis. Default is None.
        c: str, optional
            Color of the label text. Default is "blue".
        s: int, optional
            Size of the label text. Default is 10.
        
        Returns
        -------
        None
        """
        if ylabel is not None:
            ax.set_ylabel(ylabel + "→", color=c, size=s)
        
        if xlabel is not None:
            ax.set_xlabel(xlabel + "→", color=c, size=s)
            
    
    @staticmethod
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
            
    def gridlines(ax, x=True, y=True):
        """Add gridlines to the given axis."""
        ax.grid(which='major', axis=('x' if x and not y else 'y' if y and not x else 'both'),
                linestyle='--', linewidth=0.6, alpha=0.6)
        ax.minorticks_on() # Add minor ticks without tick labels.
    
    def ticks(ax, left=True, bottom=True):
        """Remove ticks from a given axis."""
        ax.tick_params(left=left, bottom=bottom, labelleft=left, labelbottom=bottom)
        if left is False or bottom is False:
            ax.minorticks_off()
            
    @staticmethod
    def figtitle(
        fig,
        title=None,
        c="red",
        s=12,
        y=1.0
    ):
        """
        Set the title for the figure.

        Parameters
        ----------
        fig: matplotlib.Figure
            Figure to add title to.
        title: str, optional
            Title for the figure. Default is None.
        c: str, optional
            Color of the title text. Default is "red".
        s: int, optional
            Size of the title text. Default is 10.
        y: float, optional
            y-position for the title placement. Default is 1.0.

        Returns
        -------
        None
        """
        
        if title is not None:
            fig.suptitle(title, size=s, y=y, color=c)

    
    