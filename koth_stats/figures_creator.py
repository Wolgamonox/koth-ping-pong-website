from datetime import timedelta, datetime

import pandas as pd
import numpy as np
import json
import io

from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns

from koth_stats.stats_creator import *


def generate_fig_summary(filename, as_bytes=False):
    """Function to plot summary of game from filename."""

    # read from file
    read_data = {}
    with open(filename) as json_file:
        read_data = json.load(json_file)

    players = read_data['players']
    transitions = read_data['transitions']
    df = pd.DataFrame({
        'Name': [list(transition.keys())[0] for transition in transitions],
        'Interval': [list(transition.values())[0] for transition in transitions]
    })

    total_duration_seconds = df['Interval'].sum()

    player_colors = {name: color for name, color in zip(
        players, sns.color_palette('Pastel1', n_colors=len(players)))}

    crowns_claimed = get_crowns_claimed(df, players)
    total_time_king = get_total_time_king(df, players)
    reign_time = get_reign_time(df, players)
    graph_vector = get_crown_transition_graph(
        df, players, total_duration_seconds)

    fig = Figure(tight_layout=True, figsize=(10, 6))
    gs = gridspec.GridSpec(2, 3)

    # Total Time as king
    ax = fig.add_subplot(gs[0, 0])
    ax.pie(total_time_king['Duration'], labels=total_time_king.index,
           autopct='%.0f%%')
    pie_wedges = ax.pie(
        total_time_king['Duration'], labels=total_time_king.index, autopct='%.0f%%')
    for pie_wedge in pie_wedges[0]:
        pie_wedge.set_edgecolor('white')
        pie_wedge.set_facecolor(player_colors[pie_wedge.get_label()])
    ax.set_title('Fraction of time as king')

    # Mean Reign time
    ax = fig.add_subplot(gs[0, 1])
    sns.boxplot(reign_time, x='Name', y='Interval',
                palette=player_colors, ax=ax)
    ax.set_xlabel('')
    ax.set_ylabel('Seconds')
    ax.set_title('Reign time')

    # Crowns claimed
    ax = fig.add_subplot(gs[0, 2])
    sns.barplot(x=crowns_claimed.index, y=crowns_claimed.Claimed,
                palette=player_colors, ax=ax)
    ax.set_yticks(range(0, int(np.ceil(crowns_claimed['Claimed'].max())) + 1))
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title('Number of crowns claimed')

    # Transition graph
    ax = fig.add_subplot(gs[1, :])
    sns.lineplot(x=range(len(graph_vector)),
                 y=graph_vector, drawstyle='steps', ax=ax)
    ax.set_xlabel('Game advancement (percent)')
    ax.set_title('Visualization of crown transitions')

    game_date = get_date_from(filename).strftime('%d/%m/%Y %H:%M:%S')

    fig.suptitle(
        'Game Summary %s\nDuration: %s\n First: %s | Last: %s' % (
            game_date,
            timedelta(seconds=int(total_duration_seconds)),
            df.iloc[0]['Name'],
            df.iloc[-1]['Name']),
    )

    for player in players:
        print('%s S= %.3f' % (player, calculate_S(player, total_time_king,
              crowns_claimed, df.iloc[-1]['Name'], total_duration_seconds)))

    if as_bytes:
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return output.get_value()
    else:
        return fig


def get_date_from(filename):
    date = filename.split(' ')[1].replace('(', '')
    time = filename.split(' ')[2].replace(').json', '')
    return datetime.strptime("%s %s" % (date, time), "%d-%m-%Y %H_%M_%S")


def save_summary(filename: str):
    fig = generate_fig_summary(filename)

    path = filename.split('.')[0] + '.png'

    fig.savefig(path)
