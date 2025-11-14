#!/usr/bin/env python3

#---------------------------------
# Author: Ankit Anand
# Date: 09/11/25
# Email: ankit0.anand0@gmail.com
#---------------------------------

from ipywidgets import Button, Label, FloatText, HBox, VBox
from matplotlib.widgets import SpanSelector
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display

def annotate(fig, axs):
    """
    Make a Matplotlib figure interactive inside JupyterLab with:
        1. Left-click to create events or regions
        2. Right-click to delete events or regions
        3. Segment-based navigation
    """

    # Ensure axs is iterable
    axs_flattened = np.ravel(np.atleast_1d(axs))

    coord_label = Label(value="Hover over the plot...")
    status_label = Label(value="Tool: None")

    mode = {"tool": None}
    regions, region_patches = [], []
    events, event_lines = [], []
    ann = []

    # UI elements
    btn_event = Button(description="Mark Event")
    btn_region = Button(description="Select Region")
    btn_prev = Button(description="<<")
    btn_next = Button(description=">>")
    segment_box = FloatText(value=10.0, description="View Size:", step=1)

    # Hover
    def hover(event):
        if event.inaxes in axs_flattened and event.xdata is not None and event.ydata is not None:
            coord_label.value = f"x = {event.xdata:.3f}, y = {event.ydata:.3f}"
        else:
            coord_label.value = "Hover over the plot..."

    # Unified click handling for both event + region tools
    def onclick(event):
        if event.inaxes not in axs_flattened or event.xdata is None:
            return
    
        ax = event.inaxes
        x = event.xdata
    
        # --- Event tool ---
        if mode["tool"] == "event":
            # RIGHT-CLICK -> delete nearest event within threshold
            if event.button == 3:
                if not events:
                    return
                # compute distances to all events
                diffs = [abs(x - xe) for xe in events]
                # threshold: keep your original idea; guard for zero/None
                try:
                    thresh = 0.02 * float(segment_box.value)
                except Exception:
                    thresh = 0.02
                # indices of events within threshold
                candidates = [i for i, d in enumerate(diffs) if d <= thresh]
                if not candidates:
                    return
                # pick nearest candidate (smallest distance)
                idx = min(candidates, key=lambda i: diffs[i])
                x_old = events.pop(idx)
                line = event_lines.pop(idx)
                # remove visual line and corresponding annotation entries
                try:
                    line.remove()
                except Exception:
                    pass
                # use tolerant comparison for ann floats (avoid exact equality)
                ann[:] = [t for t in ann if not (abs(t[0] - x_old) < 1e-6 and abs(t[1] - x_old) < 1e-6)]
                fig.canvas.draw_idle()
                status_label.value = f"Deleted event near x={x_old:.3f}"
                return
    
            # LEFT-CLICK -> add event
            if event.button == 1:
                line = ax.axvline(x, color="orange", linestyle="--", alpha=0.7)
                events.append(x)
                event_lines.append(line)
                ann.append((x, x, ""))
                fig.canvas.draw_idle()
                status_label.value = f"Marked event at x={x:.3f}"
            return
    
        # --- Region tool ---
        if mode["tool"] == "region" and event.button == 3:  # right-click delete region
            if not regions:
                return
            # find all regions that contain x
            containing = [i for i, (r, p) in enumerate(zip(regions, region_patches)) if r[0] <= x <= r[1]]
            if not containing:
                return
            # choose the region whose center is nearest to x (handles overlapping regions)
            def center_dist(i):
                rmin, rmax = regions[i]
                return abs(((rmin + rmax) / 2.0) - x)
            idx = min(containing, key=center_dist)
            rmin, rmax = regions.pop(idx)
            patch = region_patches.pop(idx)
            try:
                patch.remove()
            except Exception:
                pass
            # remove matching ann entries with tolerant comparison
            ann[:] = [t for t in ann if not (abs(t[0] - rmin) < 1e-6 and abs(t[1] - rmax) < 1e-6)]
            fig.canvas.draw_idle()
            status_label.value = f"Deleted region {rmin:.3f}–{rmax:.3f}"
            return


    # Region creation (via SpanSelector)
    span_selectors = []

    def make_onselect(ax):
        def onselect(xmin, xmax):
            if mode["tool"] != "region":
                return
            if plt.get_current_fig_manager().canvas.manager.toolbar.mode != '':
                return
            if xmin == xmax:
                return

            patch = ax.axvspan(xmin, xmax, color="orange", alpha=0.3)
            regions.append((xmin, xmax))
            region_patches.append(patch)
            ann.append((xmin, xmax, ""))
            fig.canvas.draw_idle()
            status_label.value = f"Selected region: {xmin:.3f} – {xmax:.3f}"
        return onselect

    for ax in axs_flattened:
        selector = SpanSelector(
            ax,
            make_onselect(ax),
            direction="horizontal",
            useblit=True,
            props=dict(alpha=0.2, facecolor="orange"),
            interactive=False,
            button=1
        )
        selector.set_active(False)
        span_selectors.append(selector)

    # Tool switching
    def activate_event(_):
        mode["tool"] = "event"
        for s in span_selectors:
            s.set_active(False)
        status_label.value = "Tool: Event Marker (Left click: add, Right click: delete)"

    def activate_region(_):
        mode["tool"] = "region"
        for s in span_selectors:
            s.set_active(True)
        status_label.value = "Tool: Region Selector (Left-drag: add, Right click: delete)"

    # Navigation
    def get_xlim():
        """Return the current xlim of the first axis."""
        return axs_flattened[0].get_xlim()

    def set_xlim(xmin, xmax):
        """Apply xlim to all axes and redraw."""
        for ax in axs_flattened:
            ax.set_xlim(xmin, xmax)
        fig.canvas.draw_idle()

    def update_segment_width(_):
        width = segment_box.value
        xmin, _ = get_xlim()
        xmax = xmin + width
        set_xlim(xmin, xmax)
        status_label.value = f"Segment width changed to {width:.2f}s"

    def go_prev(_):
        width = segment_box.value
        xmin, xmax = get_xlim()
        new_start = xmin - width
        set_xlim(new_start, new_start + width)
        status_label.value = f"Moved to previous segment ({new_start:.2f}s)"

    def go_next(_):
        width = segment_box.value
        xmin, xmax = get_xlim()
        new_start = xmax
        set_xlim(new_start, new_start + width)
        status_label.value = f"Moved to next segment ({new_start:.2f}s)"


    # Bind handlers
    fig.canvas.mpl_connect("motion_notify_event", hover)
    fig.canvas.mpl_connect("button_press_event", onclick)
    btn_event.on_click(activate_event)
    btn_region.on_click(activate_region)
    btn_prev.on_click(go_prev)
    btn_next.on_click(go_next)
    segment_box.observe(update_segment_width, names="value")
    
    
    # Initialize view range to first segment width
    if axs_flattened.size > 0:
        ax0 = axs_flattened[0]
        xmin, xmax = ax0.get_xlim()
        width = segment_box.value
        set_xlim(xmin, xmin + width)
        status_label.value = f"Initialized view: {xmin:.2f} – {xmin + width:.2f}s"

    # Layout
    tool_row = HBox([btn_event, btn_region, btn_prev, btn_next, segment_box])
    ui = VBox([tool_row, coord_label, status_label, fig.canvas])
    display(ui)

    return ann
