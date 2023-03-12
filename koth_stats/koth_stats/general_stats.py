import pandas as pd

from .game_stats import GameStatService

# def plot_score_for(games: list[tuple[list[str], pd.DataFrame]]):
#     """Plots the score evolution of players on multiple games.Ordered chronologically."""

#     gs_services = [GameStatService(game[0], game[1]) for game in games]

#     names = []
#     points = []
#     games = []

#     for game_id, ks_service in enumerate(gs_services):
#         points_df = ks_service.points_df()

#         names += list(points_df.index)
#         points += list(points_df.Points)
#         games += [game_id for _ in range(nb_players)]
