from datetime import timedelta, datetime

import pandas as pd
import numpy as np

from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
import seaborn as sns


def generate_summary(filename):
    """Function to plot summary of game from filename."""

    df = pd.read_csv(filename).drop('Unnamed: 0', axis=1)
    total_duration_seconds = df['Interval'].sum()

    player_names = df['Name'].unique()
    player_colors = {name: color for name, color in zip(
        player_names, sns.color_palette('Pastel1')[:len(player_names)])}

    crowns_claimed = df.drop(index=0).groupby('Name').count().rename(
        {'Interval': 'Claimed'}, axis=1).sort_values('Claimed', ascending=False)
    total_time_king = df.groupby('Name').sum().rename(
        {'Interval': 'Duration'}, axis=1).sort_values('Duration', ascending=False)
    mean_reign_time = df.groupby('Name').mean().rename(
        {'Interval': 'Duration'}, axis=1).sort_values('Duration', ascending=False)

    df['interval_perc'] = df['Interval'].apply(
        lambda x: int(np.ceil(x/total_duration_seconds * 100)))

    graph_vector = []

    for _, transition in df.iterrows():
        graph_vector.extend(
            transition.Name for i in range(transition.interval_perc))

    print('Game duration: %s ' %
          str(timedelta(seconds=int(total_duration_seconds))))
    print('First king: %s | Last king: %s ' %
          (df.iloc[0]['Name'], df.iloc[-1]['Name']))

    fig = Figure(tight_layout=True, figsize=(10, 6))
    gs = gridspec.GridSpec(2, 3)

    # Total Time as king
    ax = fig.add_subplot(gs[0, 0])
    ax.pie(total_time_king['Duration'], labels=total_time_king.index,
           autopct='%.0f%%', colors=[player_colors[key] for key in player_colors])
    ax.set_title('Fraction of time as king')

    # Mean Reign time
    ax = fig.add_subplot(gs[0, 1])
    sns.barplot(x=mean_reign_time.index, y=mean_reign_time.Duration,
                palette=player_colors, ax=ax)
    ax.set_xlabel('')
    ax.set_ylabel('Seconds')
    ax.set_title('Mean reign time')

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
        str(timedelta(seconds=int(total_duration_seconds))),
        df.iloc[0]['Name'],
        df.iloc[-1]['Name']),
    )

    return fig


def get_date_from(filename):
    date = filename.split(' ')[1].replace('(', '')
    time = filename.split(' ')[2].replace(').csv', '')
    return datetime.strptime("%s %s" % (date, time), "%d-%m-%Y %H_%M_%S")


def save_summary(filename: str):
    fig = generate_summary(filename)

    path = filename.split('.')[0] + '.png'

    fig.savefig(path)
