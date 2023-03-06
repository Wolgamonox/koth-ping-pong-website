import numpy as np
from matplotlib.axes import Axes
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure


def display_figure(fig: Figure, ax: Axes):
    """Helper function to display a ``figure.Figure`` into a ``pyplot`` figure."""
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    rgba = np.asarray(canvas.buffer_rgba())

    ax.imshow(rgba)
    ax.axis("off")
