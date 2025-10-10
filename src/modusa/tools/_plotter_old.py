#!/usr/bin/env python3


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Helper for 2D plot
def _calculate_extent(x, y):
	# Handle spacing safely
	if len(x) > 1:
		dx = x[1] - x[0]
	else:
		dx = 1  # Default spacing for single value
	if len(y) > 1:
		dy = y[1] - y[0]
	else:
		dy = 1  # Default spacing for single value
		
	return [
		x[0] - dx / 2,
		x[-1] + dx / 2,
		y[0] - dy / 2,
		y[-1] + dy / 2
	]
	
# Helper to load fonts (devnagri)
def set_default_hindi_font():
	"""
	Hindi fonts works for both english and hindi.
	"""
	from pathlib import Path
	import matplotlib as mpl
	import matplotlib.font_manager as fm
	# Path to your bundled font
	font_path = Path(__file__).resolve().parents[1] / "fonts" / "NotoSansDevanagari-Regular.ttf"
	
	# Register the font with matplotlib
	fm.fontManager.addfont(str(font_path))
	
	# Get the font family name from the file
	hindi_font = fm.FontProperties(fname=str(font_path))
	
	# Set as default rcParam
	mpl.rcParams['font.family'] = hindi_font.get_name()

#set_default_hindi_font()

#======== 1D ===========
def plot1d(*args, ann=None, events=None, xlim=None, ylim=None, xlabel=None, ylabel=None, title=None, legend=None, fmt=None, show_grid=False, show_stem=False):
		"""
		Plots a 1D signal using matplotlib.

		.. code-block:: python
	
			import modusa as ms
			import numpy as np
			
			x = np.arange(100) / 100
			y = np.sin(x)
			
			display(ms.plot1d(y, x))
			
	
		Parameters
		----------
		*args : tuple[array-like, array-like] | tuple[array-like]
			- The signal y and axis x to be plotted.
			- If only values are provided, we generate the axis using arange.
			- E.g. (y1, x1), (y2, x2), ...
		ann : list[tuple[Number, Number, str] | None
			- A list of annotations to mark specific points. Each tuple should be of the form (start, end, label).
			- Default: None => No annotation.
		events : list[Number] | None
			- A list of x-values where vertical lines (event markers) will be drawn.
			- Default: None
		xlim : tuple[Number, Number] | None
			- Limits for the x-axis as (xmin, xmax).
			- Default: None
		ylim : tuple[Number, Number] | None
			- Limits for the y-axis as (ymin, ymax).
			- Default: None
		xlabel : str | None
			- Label for the x-axis.
			- - Default: None
		ylabel : str | None
			- Label for the y-axis.
			- Default: None
		title : str | None
			- Title of the plot.
			- Default: None
		legend : list[str] | None
			- List of legend labels corresponding to each signal if plotting multiple lines.
			- Default: None
		fmt: list[str] | None
			- linefmt for different line plots.
			- Default: None
		show_grid: bool
			- If you want to show the grid.
			- Default: False
		show_stem: bool:
			- If you want stem plot.
			- Default: False
	
		Returns
		-------
		plt.Figure
			Matplolib figure.
		"""
		for arg in args:
			if len(arg) not in [1, 2]: # 1 if it just provides values, 2 if it provided axis as well
				raise ValueError(f"1D signal needs to have max 2 arrays (y, x) or simply (y, )")
			
		if isinstance(legend, str): legend = (legend, )
		if legend is not None:
			if len(legend) < len(args):
				raise ValueError(f"`legend` should be provided for each signal.")
		
		if isinstance(fmt, str): fmt = [fmt]
		if fmt is not None:
			if len(fmt) < len(args):
				raise ValueError(f"`fmt` should be provided for each signal.")

		colors = plt.get_cmap('tab10').colors

		fig = plt.figure(figsize=(16, 2))
		gs = gridspec.GridSpec(3, 1, height_ratios=[0.2, 0.2, 1])
		
		signal_ax = fig.add_subplot(gs[2, 0])
		annotation_ax = fig.add_subplot(gs[0, 0], sharex=signal_ax)
		events_ax = fig.add_subplot(gs[1, 0])
		
		# Set lim
		if xlim is not None:
			signal_ax.set_xlim(xlim)
		
		if ylim is not None:
			signal_ax.set_ylim(ylim)
			
		# Add signal plot
		for i, signal in enumerate(args):
			if len(signal) == 1:
				y = signal[0]
				x = np.arange(y.size)
				if legend is not None:
					if show_stem is True:
						markerline, stemlines, baseline = signal_ax.stem(x, y, label=legend[i])
						markerline.set_color(colors[i])
						stemlines.set_color(colors[i])
						baseline.set_color("k")
					else:
						if fmt is not None:
							signal_ax.plot(x, y, fmt[i], markersize=4, label=legend[i])
						else:
							signal_ax.plot(x, y, color=colors[i], label=legend[i])
				else:
					if show_stem is True:
						markerline, stemlines, baseline = signal_ax.stem(x, y)
						markerline.set_color(colors[i])
						stemlines.set_color(colors[i])
						baseline.set_color("k")
					else:
						if fmt is not None:
							signal_ax.plot(x, y, fmt[i], markersize=4)
						else:
							signal_ax.plot(x, y, color=colors[i])
						
			elif len(signal) == 2:
				y, x = signal[0], signal[1]
				if legend is not None:
					if show_stem is True:
						markerline, stemlines, baseline = signal_ax.stem(x, y, label=legend[i])
						markerline.set_color(colors[i])
						stemlines.set_color(colors[i])
						baseline.set_color("k")
					else:
						if fmt is not None:
							signal_ax.plot(x, y, fmt[i], markersize=4, label=legend[i])
						else:
							signal_ax.plot(x, y, color=colors[i], label=legend[i])
				else:
					if show_stem is True:
						markerline, stemlines, baseline = signal_ax.stem(x, y)
						markerline.set_color(colors[i])
						stemlines.set_color(colors[i])
						baseline.set_color("k")
					else:
						if fmt is not None:
							signal_ax.plot(x, y, fmt[i], markersize=4)
						else:
							signal_ax.plot(x, y, color=colors[i])
							
		
		# Add annotations
		if ann is not None:
			annotation_ax.set_ylim(0, 1) # For consistent layout
			# Determine visible x-range
			x_view_min = xlim[0] if xlim is not None else np.min(x)
			x_view_max = xlim[1] if xlim is not None else np.max(x)
			
			for i, (start, end, tag) in enumerate(ann):
				# We make sure that we only plot annotation that are within the x range of the current view
				if start >= x_view_max or end <= x_view_min:
					continue
				
				# Clip boundaries to xlim
				start = max(start, x_view_min)
				end = min(end, x_view_max)
				
				box_colors = ["gray", "lightgray"] # Alternates color between two
				box_color = box_colors[i % 2]
				
				width = end - start
				rect = Rectangle((start, 0), width, 1, color=box_color, alpha=0.7)
				annotation_ax.add_patch(rect)
				
				text_obj = annotation_ax.text(
					(start + end) / 2, 0.5, tag,
					ha='center', va='center',
					fontsize=10, color="black", fontweight='bold', zorder=10, clip_on=True
				)
				
				text_obj.set_clip_path(rect)
				
				
		# Add vlines
		if events is not None:
#			if not isinstance(events, tuple):
#				raise TypeError(f"`events` should be tuple, got {type(events)}")
			
			for xpos in events:
				if xlim is not None:
					if xlim[0] <= xpos <= xlim[1]:
						annotation_ax.axvline(x=xpos, color='red', linestyle='-', linewidth=1.5)
				else:
					annotation_ax.axvline(x=xpos, color='red', linestyle='-', linewidth=1.5)
					
		# Add legend
		if legend is not None:
			handles, labels = signal_ax.get_legend_handles_labels()
			fig.legend(handles, labels, loc='upper right', bbox_to_anchor=(0.9, 1.2), ncol=len(legend), frameon=True)
			
		# Set title, labels
		if title is not None:
			annotation_ax.set_title(title, pad=10, size=11)
		if xlabel is not None:
			signal_ax.set_xlabel(xlabel)
		if ylabel is not None:
			signal_ax.set_ylabel(ylabel)
			
		# Add grid to the plot
		if show_grid is True:
			signal_ax.grid(True, linestyle=':', linewidth=0.7, color='gray', alpha=0.7)
		
		# Remove the boundaries and ticks from an axis
		if ann is not None:
			annotation_ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
		else:
			annotation_ax.axis("off")
			
		if events is not None:
			events_ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
		else:
			events_ax.axis("off")
		
		
		fig.subplots_adjust(hspace=0.01, wspace=0.05)
		plt.close()
		return fig

#======== 2D ===========
def plot2d(*args, ann=None, events=None, xlim=None, ylim=None, origin="lower", Mlabel=None, xlabel=None, ylabel=None, title=None, legend=None, lm=False, show_grid=False):
	"""
	Plots a 2D matrix (e.g., spectrogram or heatmap) with optional annotations and events.

	.. code-block:: python

		import modusa as ms
		import numpy as np
		
		M = np.random.random((10, 30))
		y = np.arange(M.shape[0])
		x = np.arange(M.shape[1])
		
		display(ms.plot2d(M, y, x))

	Parameters
	----------
	*args : tuple[array-like, array-like]
		- The signal values to be plotted.
		- E.g. (M1, y1, x1), (M2, y2, x2), ...
	ann : list[tuple[Number, Number, str]] | None
		- A list of annotation spans. Each tuple should be (start, end, label).
		- Default: None (no annotations).
	events : list[Number] | None
		- X-values where vertical event lines will be drawn.
		- Default: None.
	xlim : tuple[Number, Number] | None
		- Limits for the x-axis as (xmin, xmax).
		- Default: None (auto-scaled).
	ylim : tuple[Number, Number] | None
		- Limits for the y-axis as (ymin, ymax).
		- Default: None (auto-scaled).
	origin : {'upper', 'lower'}
		- Origin position for the image display. Used in `imshow`.
		- Default: "lower".
	Mlabel : str | None
		- Label for the colorbar (e.g., "Magnitude", "Energy").
		- Default: None.
	xlabel : str | None
		- Label for the x-axis.
		- Default: None.
	ylabel : str | None
		- Label for the y-axis.
		- Default: None.
	title : str | None
		- Title of the plot.
		- Default: None.
	legend : list[str] | None
		- Legend labels for any overlaid lines or annotations.
		- Default: None.
	lm: bool
		- Adds a circular marker for the line.
		- Default: False
		- Useful to show the data points.
	show_grid: bool
		- If you want to show the grid.
		- Default: False

	Returns
	-------
	matplotlib.figure.Figure
		The matplotlib Figure object.
	"""
	
	for arg in args:
		if len(arg) not in [1, 2, 3]: # Either provide just the matrix or with both axes info
			raise ValueError(f"Data to plot needs to have 3 arrays (M, y, x)")
	if isinstance(legend, str): legend = (legend, )
	
	fig = plt.figure(figsize=(16, 4))
	gs = gridspec.GridSpec(3, 1, height_ratios=[0.2, 0.1, 1]) # colorbar, annotation, signal

	colors = plt.get_cmap('tab10').colors
	
	signal_ax = fig.add_subplot(gs[2, 0])
	annotation_ax = fig.add_subplot(gs[1, 0], sharex=signal_ax)
	
	colorbar_ax = fig.add_subplot(gs[0, 0])
	colorbar_ax.axis("off")
	
	
	# Add lim
	if xlim is not None:
		signal_ax.set_xlim(xlim)
		
	if ylim is not None:
		signal_ax.set_ylim(ylim)
		
	# Add signal plot
	i = 0 # This is to track the legend for 1D plots
	for signal in args:
		
		data = signal[0] # This can be 1D or 2D (1D meaning we have to overlay on the matrix)
			
		if data.ndim == 1: # 1D
			if len(signal) == 1: # It means that the axis was not passed
				x = np.arange(data.shape[0])
			else:
				x = signal[1]
			
			if lm is False:
				if legend is not None:
					signal_ax.plot(x, data, label=legend[i])
					signal_ax.legend(loc="upper right")
				else:
					signal_ax.plot(x, data)
			else:
				if legend is not None:
					signal_ax.plot(x, data, marker="o", markersize=7, markerfacecolor='red', linestyle="--", linewidth=2, label=legend[i])
					signal_ax.legend(loc="upper right")
				else:
					signal_ax.plot(x, data, marker="o", markersize=7, markerfacecolor='red', linestyle="--", linewidth=2)
					
			i += 1
			
		elif data.ndim == 2: # 2D
			M = data
			if len(signal) == 1: # It means that the axes were not passed
				y = np.arange(M.shape[0])
				x = np.arange(M.shape[1])
				extent = _calculate_extent(x, y)
				im = signal_ax.imshow(M, aspect="auto", origin=origin, cmap="gray_r", extent=extent)
				
			elif len(signal) == 3: # It means that the axes were passed
				M, y, x = signal[0], signal[1], signal[2]
				extent = _calculate_extent(x, y)
				im = signal_ax.imshow(M, aspect="auto", origin=origin, cmap="gray_r", extent=extent)
	
	# Add annotations
	if ann is not None:
		annotation_ax.set_ylim(0, 1) # For consistent layout
		# Determine visible x-range
		x_view_min = xlim[0] if xlim is not None else np.min(x)
		x_view_max = xlim[1] if xlim is not None else np.max(x)
		
		for i, (start, end, tag) in enumerate(ann):
			# We make sure that we only plot annotation that are within the x range of the current view
			if start >= x_view_max or end <= x_view_min:
				continue
			
			# Clip boundaries to xlim
			start = max(start, x_view_min)
			end = min(end, x_view_max)
				
			color = colors[i % len(colors)]
			width = end - start
			rect = Rectangle((start, 0), width, 1, color=color, alpha=0.7)
			annotation_ax.add_patch(rect)
			text_obj = annotation_ax.text(
				(start + end) / 2, 0.5, tag,
				ha='center', va='center',
				fontsize=10, color='white', fontweight='bold', zorder=10, clip_on=True
			)
			
			text_obj.set_clip_path(rect)
			
	# Add vlines
	if events is not None:
		for xpos in events:
			if xlim is not None:
				if xlim[0] <= xpos <= xlim[1]:
					annotation_ax.axvline(x=xpos, color='black', linestyle='--', linewidth=1.5)
			else:
				annotation_ax.axvline(x=xpos, color='black', linestyle='--', linewidth=1.5)
	
	# Add legend incase there are 1D overlays
	if legend is not None:
		handles, labels = signal_ax.get_legend_handles_labels()
		if handles:  # Only add legend if there's something to show
			signal_ax.legend(handles, labels, loc="upper right")
	
	# Add colorbar
	# Create an inset axis on top-right of signal_ax
	cax = inset_axes(
		colorbar_ax,
		width="20%",      # percentage of parent width
		height="20%",      # height in percentage of parent height
		loc='upper right',
		bbox_to_anchor=(0, 0, 1, 1),
		bbox_transform=colorbar_ax.transAxes,
		borderpad=1
	)
	
	cbar = plt.colorbar(im, cax=cax, orientation='horizontal')
	cbar.ax.xaxis.set_ticks_position('top')
	
	if Mlabel is not None:
		cbar.set_label(Mlabel, labelpad=5)
	
		
	# Set title, labels
	if title is not None:
		annotation_ax.set_title(title, pad=10, size=11)
	if xlabel is not None:
		signal_ax.set_xlabel(xlabel)
	if ylabel is not None:
		signal_ax.set_ylabel(ylabel)
		
	# Add grid to the plot
	if show_grid is True:
		signal_ax.grid(True, linestyle=':', linewidth=0.7, color='gray', alpha=0.7)
	
	# Making annotation axis spines thicker
	if ann is not None:
		annotation_ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
	else:
		annotation_ax.axis("off")

	fig.subplots_adjust(hspace=0.01, wspace=0.05)
	plt.close()
	return fig

#======== Plot distribution ===========
def plot_dist(*args, ann=None, xlim=None, ylim=None, ylabel=None, xlabel=None, title=None, legend=None, show_hist=True, npoints=200, bins=30):
		"""
		Plot distribution.

		.. code-block:: python
			
			import modusa as ms
			import numpy as np
			np.random.seed(42)
			data = np.random.normal(loc=1, scale=1, size=1000)
			ms.plot_dist(data, data+5, data-10, ann=[(0, 1, "A")], legend=("D1", "D2", "D3"), ylim=(0, 1), xlabel="X", ylabel="Counts", title="Distribution")

		Parameters
		----------
		*args: ndarray
			- Data arrays for which distribution needs to be plotted.
			- Arrays will be flattened.
		ann : list[tuple[Number, Number, str] | None
			- A list of annotations to mark specific points. Each tuple should be of the form (start, end, label).
			- Default: None => No annotation.
		events : list[Number] | None
			- A list of x-values where vertical lines (event markers) will be drawn.
			- Default: None
		xlim : tuple[Number, Number] | None
			- Limits for the x-axis as (xmin, xmax).
			- Default: None
		ylim : tuple[Number, Number] | None
			- Limits for the y-axis as (ymin, ymax).
			- Default: None
		xlabel : str | None
			- Label for the x-axis.
			- - Default: None
		ylabel : str | None
			- Label for the y-axis.
			- Default: None
		title : str | None
			- Title of the plot.
			- Default: None
		legend : list[str] | None
			- List of legend labels corresponding to each signal if plotting multiple distributions.
			- Default: None
		show_hist: bool
			- Want to show histogram as well.
		npoints: int
			- Number of points for which gaussian needs to be computed between min and max.
			- Higher value means more points are evaluated with the fitted gaussian, thereby higher resolution.
		bins: int
			- The number of bins for histogram.
			- This is used only to plot the histogram.

		Returns
		-------
		plt.Figure
			- Matplotlib figure.
		"""
		from scipy.stats import gaussian_kde
	
		if isinstance(legend, str):
			legend = (legend, )
			
		if legend is not None:
			if len(legend) < len(args):
				raise ValueError(f"Legend should be provided for each signal.")
					
		# Create figure
		fig = plt.figure(figsize=(16, 4))
		gs = gridspec.GridSpec(2, 1, height_ratios=[0.1, 1])
	
		colors = plt.get_cmap('tab10').colors
	
		dist_ax = fig.add_subplot(gs[1, 0])
		annotation_ax = fig.add_subplot(gs[0, 0], sharex=dist_ax)
	
		# Set limits
		if xlim is not None:
			dist_ax.set_xlim(xlim)
			
		if ylim is not None:
			dist_ax.set_ylim(ylim)
			
		# Add plot
		for i, data in enumerate(args):
			# Fit gaussian to the data
			kde = gaussian_kde(data)
		
			# Create points to evaluate KDE
			x = np.linspace(np.min(data), np.max(data), npoints)
			y = kde(x)
		
			if legend is not None:
				dist_ax.plot(x, y, color=colors[i], label=legend[i])
				if show_hist is True:
					dist_ax.hist(data, bins=bins, density=True, alpha=0.3, facecolor=colors[i], edgecolor='black', label=legend[i])
			else:
				dist_ax.plot(x, y, color=colors[i])
				if show_hist is True:
					dist_ax.hist(data, bins=bins, density=True, alpha=0.3, facecolor=colors[i], edgecolor='black')
							
		# Add annotations
		if ann is not None:
			annotation_ax.set_ylim(0, 1) # For consistent layout
			# Determine visible x-range
			x_view_min = xlim[0] if xlim is not None else np.min(x)
			x_view_max = xlim[1] if xlim is not None else np.max(x)
			for i, (start, end, tag) in enumerate(ann):
				# We make sure that we only plot annotation that are within the x range of the current view
				if start >= x_view_max or end <= x_view_min:
					continue
				
				# Clip boundaries to xlim
				start = max(start, x_view_min)
				end = min(end, x_view_max)
					
				color = colors[i % len(colors)]
				width = end - start
				rect = Rectangle((start, 0), width, 1, color=color, alpha=0.7)
				annotation_ax.add_patch(rect)
			
				text_obj = annotation_ax.text((start + end) / 2, 0.5, tag, ha='center', va='center', fontsize=10, color='white', fontweight='bold', zorder=10, clip_on=True)
				text_obj.set_clip_path(rect)
					
		# Add legend
		if legend is not None:
			handles, labels = dist_ax.get_legend_handles_labels()
			fig.legend(handles, labels, loc='upper right', bbox_to_anchor=(0.9, 1.1), ncol=len(legend), frameon=True)
			
		# Set title, labels
		if title is not None:
			annotation_ax.set_title(title, pad=10, size=11)
		if xlabel is not None:
			dist_ax.set_xlabel(xlabel)
		if ylabel is not None:
			dist_ax.set_ylabel(ylabel)
			
		# Remove the boundaries and ticks from annotation axis
		if ann is not None:
			annotation_ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
		else:
			annotation_ax.axis("off")
			
		fig.subplots_adjust(hspace=0.01, wspace=0.05)
		plt.close()
		return fig