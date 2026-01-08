import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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
        
    for i, (utt_id, ch, start, end, label, confidence, group) in enumerate(ann):
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
