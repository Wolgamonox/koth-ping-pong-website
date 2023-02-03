from datetime import timedelta, datetime

import pandas as pd
import numpy as np
import json

from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
import seaborn as sns


def generate_plot_summary(filename):
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
    pie_wedges = ax.pie(total_time_king['Duration'], labels=total_time_king.index, autopct='%.0f%%')
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
        print('%s S= %.3f' % (player, calculate_S(player, total_time_king, crowns_claimed, df.iloc[-1]['Name'], total_duration_seconds)))

    return fig

def calculate_S(player, total_time_king, crowns_claimed, last_king, game_duration):
    alpha = 15
    beta = 3 * game_duration
    gamma = 5 * game_duration

    t = total_time_king.loc[player]['Duration']
    c = crowns_claimed.loc[player]['Claimed']
    w = 1 if last_king == player else 0

    return (alpha * t + beta * c + gamma * w) / game_duration


def get_crowns_claimed(df, players):
    first_king = df.iloc[0]['Name']

    crowns_claimed = df.groupby('Name').count().rename(
        {'Interval': 'Claimed'}, axis=1).sort_values('Claimed', ascending=False)
    crowns_claimed.loc[first_king]['Claimed'] -= 1

    # include other players
    if len(crowns_claimed) < len(players):
        for player in players:
            if player not in crowns_claimed.index:
                crowns_claimed = pd.concat(
                    [crowns_claimed, pd.DataFrame({'Claimed': 0}, index=[player])])

    return crowns_claimed


def get_total_time_king(df, players):
    total_time_king = df.groupby('Name').sum().rename(
        {'Interval': 'Duration'}, axis=1).sort_values('Duration', ascending=False)

    # include other players
    if len(total_time_king) < len(players):
        for player in players:
            if player not in total_time_king.index:
                total_time_king = pd.concat(
                    [total_time_king, pd.DataFrame({'Duration': 0}, index=[player])])

    return total_time_king


def get_reign_time(df, players):
    reign_time = df

    # include other players
    if len(reign_time['Name'].unique()) < len(players):
        for player in players:
            if player not in reign_time['Name'].unique():
                reign_time = pd.concat(
                    [reign_time, pd.DataFrame({'Name': [player], 'Interval':[0]})])

    return reign_time


def get_crown_transition_graph(df, players, total_duration_seconds):
    df['interval_perc'] = df['Interval'].apply(
        lambda x: int(np.ceil(x/total_duration_seconds * 100)))

    graph_vector = []
    for _, transition in df.iterrows():
        graph_vector.extend(
            transition.Name for i in range(transition.interval_perc))

    return graph_vector


def get_date_from(filename):
    date = filename.split(' ')[1].replace('(', '')
    time = filename.split(' ')[2].replace(').json', '')
    return datetime.strptime("%s %s" % (date, time), "%d-%m-%Y %H_%M_%S")


def save_summary(filename: str):
    fig = generate_plot_summary(filename)

    path = filename.split('.')[0] + '.png'

    fig.savefig(path)
