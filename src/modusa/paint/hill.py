import matplotlib.pyplot as plt
import numpy as np

def hill(
    ax,
    distributions,
    labels=None,
    ylabel=None,
    xlabel=None,
    xlim=None,
    title=None,
    widths=0.7,
    bw_method=0.3,
    jitter_amount=0.1,
    side="upper",
    show_stats=True,
):
    """
    A plot to see distribution of different groups
    along with statistical markers.

    Parameters
    ----------
    ax: matplotlib axes, optional
        Axes to plot on.
    distributions: list[arrays]
        List of each group data arrays for which hill plot needs to be plotted.
    labels: list of str, optional
        Labels for each group (y-axis).
    xlabel: str, optional
        Label for x-axis.
    ylabel: str, optional
        Label for y-axis.
    xlim: tuple[float, float] | None
        xlim (Default: None)
    title: str, optional
        Plot title.
    widths: float, optional
        Width of violins.
    bw_method: float, optional
        Bandwidth method for KDE.
    jitter_amount: float, optional
        Amount of vertical jitter for strip points.
    side: str, 'upper' or 'lower'
        Which half of the violin to draw (upper or lower relative to y-axis).
    show_stats: bool, optional
        Whether to show mean and median markers.
    """
    
    plt.style.use("default")  # Not supporting dark mode
    plt.rcParams["font.family"] = "DejaVu Sans"  # Devnagari not needed for this.
    
    created_fig = False
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, len(distributions) * 1.5))
        created_fig = True
        
    n = len(distributions)
    
    # Default labels/colors
    if labels is None:
        labels = [f"Group {i}" for i in range(1, n + 1)]
    if isinstance(labels, str):
        labels = [labels]
        
    colors = plt.cm.tab10.colors
    if len(colors) < n:
        colors = [colors[i % len(colors)] for i in range(n)]  # Repeat colors
        
        # --- Half-violin ---
    parts = ax.violinplot(
        distributions,
        vert=False,
        showmeans=False,
        showmedians=False,
        widths=widths,
        bw_method=bw_method,
    )
    
    # Remove the default bar lines from violin plot
    for key in ["cbars", "cmins", "cmaxes", "cmedians"]:
        if key in parts:
            parts[key].set_visible(False)
            
            # Clip violin bodies to show only upper or lower half
    for i, pc in enumerate(parts["bodies"]):
        verts = pc.get_paths()[0].vertices
        y_center = i + 1  # Center y-position for this violin
        
        if side == "upper":
            verts[:, 1] = np.maximum(verts[:, 1], y_center)
        else:  # 'lower'
            verts[:, 1] = np.minimum(verts[:, 1], y_center)
        
        pc.set_facecolor(colors[i])
        pc.set_edgecolor(colors[i])
        pc.set_linewidth(1.5)
        pc.set_alpha(0.3)
        
        # --- Strip points with jitter ---
    for i, x in enumerate(distributions, start=1):
        x = np.asarray(x)
        if x.ndim != 1:
            raise ValueError("Each distribution must be 1D, make sure you are passing distributions as list of arrays [dist1(1D), dist2(1D), ...]")
        jitter = (np.random.rand(len(x)) - 0.5) * jitter_amount
        y_positions = np.full(len(x), i) + jitter
        ax.scatter(
            x,
            y_positions,
            color=colors[i - 1],
            alpha=0.6,
            s=25,
            edgecolor="white",
            linewidth=0.8,
            zorder=2,
        )
        
        # --- Statistical markers on violin distribution curve ---
    if show_stats:
        for i, (pc, x) in enumerate(zip(parts["bodies"], distributions), start=1):
            x = np.array(x)
            median_val = np.median(x)
            mean_val = np.mean(x)
            std_val = np.std(x)
            
            # Get the violin curve vertices
            verts = pc.get_paths()[0].vertices
            
            # Find y-position on violin curve for median
            median_mask = np.abs(verts[:, 0] - median_val) < (np.ptp(x) * 0.01)
            if median_mask.any():
                median_y = (
                    np.max(verts[median_mask, 1])
                    if side == "upper"
                    else np.min(verts[median_mask, 1])
                )
            else:
                median_y = i + widths / 2 if side == "upper" else i - widths / 2
                
                # Find y-position on violin curve for mean
            mean_mask = np.abs(verts[:, 0] - mean_val) < (np.ptp(x) * 0.01)
            if mean_mask.any():
                mean_y = (
                    np.max(verts[mean_mask, 1])
                    if side == "upper"
                    else np.min(verts[mean_mask, 1])
                )
            else:
                mean_y = i + widths / 2 if side == "upper" else i - widths / 2
                
                # Triangle offset from curve
            triangle_offset = 0.05
            
            # Mean marker - triangle below curve pointing up
            ax.scatter(mean_val, mean_y - triangle_offset, marker="^", s=30, facecolor=colors[i - 1], edgecolor="black", linewidth=0.5, zorder=6, label="Mean" if i == 1 else "")
            
            # Mean value text - below the triangle
            ax.text(mean_val, mean_y - triangle_offset - 0.07, f"mean: {mean_val:.2f} ± {std_val:.2f}", ha="center", va="top", fontsize=8, color="black", zorder=7)
            
            # Median marker - triangle above curve pointing down
            ax.scatter(median_val, median_y + triangle_offset, marker="v", s=30, facecolor=colors[i - 1], edgecolor="black", linewidth=0.5, zorder=6, label="Median" if i == 1 else "")
            
            # Median value text - above the triangle
            ax.text(median_val, median_y + triangle_offset + 0.07, f"median: {median_val:.2f}", ha="center", va="bottom", fontsize=8, color="black", zorder=7)
            
            # --- Labels & formatting ---
    ax.set_yticks(range(1, n + 1))
    ax.set_yticklabels(labels, fontsize=9)
    ax.tick_params(axis="x", labelsize=9)
    
    if side == "lower":
        ax.set_ylim(0.2, n + 0.5)
    else:
        ax.set_ylim(0.5, n + 0.5)
        
        # Style improvements
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.3, linestyle="--", linewidth=0.5)
    
    if xlim is not None:
        ax.set_xlim(xlim)
    
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=9)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=9)
    if title:
        ax.set_title(title, fontsize=10, pad=20)
        
    plt.tight_layout()
    plt.close()
    return fig
