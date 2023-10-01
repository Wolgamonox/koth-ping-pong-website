import random

import numpy as np
import pandas as pd
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


def generate_random_game(nb_players: int, nb_transitions: int, min_duration=0, max_duration=100):
    if nb_players < 3:
        nb_players = 3
    elif nb_players > 26:
        nb_players = 26

    players = ["Player %s" % chr(i) for i in range(65, 65 + nb_players)]

    transitions_df = pd.DataFrame(
        {
            "Name": random.choices(players, k=nb_transitions),
            "Duration": [random.randint(min_duration, max_duration) for _ in range(nb_transitions)],
        }
    )

    return players, transitions_df
