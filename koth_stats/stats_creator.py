import pandas as pd
import numpy as np


def calculate_S(player, total_time_king, crowns_claimed, last_king, game_duration):
    """This is a work in progress"""
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


def get_crown_transition_graph(df, total_duration_seconds):
    df['interval_perc'] = df['Interval'].apply(
        lambda x: int(np.ceil(x/total_duration_seconds * 100)))

    graph_vector = []
    for _, transition in df.iterrows():
        graph_vector.extend(transition.Name for _ in range(transition.interval_perc))

    return graph_vector


