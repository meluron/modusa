#!/usr/bin/env python3

from modusa.models.s1d import S1D
from modusa.models.s2d import S2D
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import itertools

def _in_notebook() -> bool:
	"""
	To check if we are in jupyter notebook environment.
	"""
	try:
		from IPython import get_ipython
		shell = get_ipython()
		return shell and shell.__class__.__name__ == "ZMQInteractiveShell"
	except ImportError:
		return False

def plot_multiple_signals(
	*args,
	loc = None,
	x_lim: tuple[float, float] | None = None,
	highlight_regions: list[tuple[float, float, str]] | None = None,
	vlines: list[float, ...] | None = None,
) -> plt.Figure:
	"""
	Plots multiple instances of uniform `Signal1D` and `Signal2D`
	with proper formatting and time aligned.

	Parameters
	----------
	loc: tuple[int]
		- The len should match the number of signals sent as args.
		- e.g. (0, 1, 1) => First plot at ax 0, second and third plot at ax 1
		- Default: None => (0, 1, 2, ...) all plots on a new ax.
	highlight_regions: list[tuple[float, float, str]]
		-
	
	"""
	
	assert len(args) >= 1, "No signal provided to plot"
	signals = args
	
	for signal in signals: 
		if not isinstance(signal, (S1D, S2D)):
			raise TypeError(f"Invalid signal type {type(signal)}")
	
	if loc is None: # => We will plot all the signals on different subplots
		loc = tuple([i for i in range(len(args))]) # Create (0, 1, 2, ...) that serves as ax number for plots
	else: # Incase loc is provided, we make sure that we do it for each of the signals
		assert len(args) == len(loc)
	
	# Make sure that all the elements in loc do not miss any number in between (0, 1, 1, 2, 4) -> Not allowed
	assert min(loc) == 0
	max_loc = max(loc)
	for i in range(max_loc):
		if i not in loc:
			raise ValueError(f"Invalid `loc` values, it should not have any missing integer in between.")
	
	# Create a dict that maps subplot to signals that need to be plotted on that subplot e.g. {0: [signal1, signal3], ...}
	subplot_signal_map = defaultdict(list)
	for signal, i in zip(args, loc):
		subplot_signal_map[i].append(signal)
	
	# We need to create a figure with right configurations
	height_ratios = []
	height_1d_subplot = 0.4
	height_2d_subplot = 1
	n_1d_subplots = 0
	n_2d_subplots = 0
	for l, signals in subplot_signal_map.items():

		# If there is any 2D signal, the subplot will be 2D
		if any(isinstance(s, S2D) for s in signals):
			n_2d_subplots += 1
			height_ratios.append(height_2d_subplot)
		
		# If all are 1D signal, the subplot will be 1D
		elif all(isinstance(s, S1D) for s in signals):
			n_1d_subplots += 1
			height_ratios.append(height_1d_subplot)
	
	
	n_subplots = n_1d_subplots + n_2d_subplots
	fig_width = 15
	fig_height = n_1d_subplots * 2 + n_2d_subplots * 4 # This is as per the figsize height set in the plotter tool
	fig, axs = plt.subplots(n_subplots, 2, figsize=(fig_width, fig_height), width_ratios=[1, 0.01], height_ratios=height_ratios) # 2nd column for cbar
	
	if n_subplots == 1:
		axs = [axs]  # axs becomes list of one pair [ (ax, cbar_ax) ]
	
	# We find the x axis limits as per the max limit for all the signals combined, so that all the signals can be seen.
	if x_lim is None:
		x_min = min(np.min(signal.x.values) for signal in args)
		x_max = max(np.max(signal.x.values) for signal in args)
		x_lim = (x_min, x_max)
		
	for l, signals in subplot_signal_map.items():
		# Incase we have plot multiple signals in the same subplot, we change the color
		fmt_cycle = itertools.cycle(['k-', 'r-', 'g-', 'b-', 'm-', 'c-', 'y-'])
		
		# For each subplot, we want to know if it is 2D or 1D
		if any(isinstance(s, S2D) for s in signals): is_1d_subplot = False
		else: is_1d_subplot = True
		
		if is_1d_subplot: # All the signals are 1D
			for signal in signals:
				fmt = next(fmt_cycle)
				if len(signals) == 1: # highlight region works properly only if there is one signal for a subplot
					signal.plot(axs[l][0], x_lim=x_lim, highlight_regions=highlight_regions, show_grid=True, vlines=vlines, fmt=fmt, legend=signal._title)
				else:
					y, x = signal._x._values, signal._y._values
					signal.plot(axs[l][0], x_lim=x_lim, show_grid=True, vlines=vlines, fmt=fmt, legend=signal.title, y_label=signal.y.label, x_label=signal.x.label, title="")
				
			# Remove the colorbar column (if the subplot is 1d)
			axs[l][1].remove()
			
		if not is_1d_subplot: # Atleast 1 signal is 2D, we we have a 2D subplot
			for signal in signals:
				if len(signals) == 1: # Only one 2D signal is to be plotted
					signal.plot(axs[l][0], x_lim=x_lim, show_colorbar=True, cax=axs[l][1], highlight_regions=highlight_regions, vlines=vlines)
				else:
					if isinstance(signal, S1D):
						fmt = next(fmt_cycle)
						signal.plot(axs[l][0], x_lim=x_lim, show_grid=True, vlines=vlines, fmt=fmt, legend=signal.title, y_label=signal.y.label, x_label=signal.x.label, title="")
					elif isinstance(signal, S2D):
						signal.plot(axs[l][0], x_lim=x_lim, show_colorbar=True, cax=axs[l][1], vlines=vlines, x_label=signal.x.label, y_label=signal.y.label, title="")
		
		# We set the xlim, this will align all the signals automatically as they are on the same row
		for l in range(n_subplots):
			axs[l][0].set_xlim(x_lim)
		
	if _in_notebook():
		plt.tight_layout()
		plt.close(fig)
		return fig
	else:
		plt.tight_layout()
		plt.show()
		return fig