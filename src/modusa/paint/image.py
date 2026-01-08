import numpy as np
import matplotlib.pyplot as plt

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
