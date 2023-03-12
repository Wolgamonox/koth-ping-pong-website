import math

import matplotlib as mpl
import pandas as pd
import pytest

import koth_stats.game_stats as gs


@pytest.fixture
def game_service():
    players = ["A", "B", "C"]

    transitions_df = pd.DataFrame(
        {
            "Name": players,
            "Duration": [10, 20, 30],
        }
    )

    return gs.GameStatService(players, transitions_df)


class TestGameservice:
    def test_initialization(self, game_service):
        assert game_service.players[0] == "A"

    def test_points(self, game_service: gs.GameStatService):
        points_df = pd.DataFrame(
            index=["A", "B", "C"],
            data={"Points": [0, 0, 0]},
        )

        points_df += game_service.total_reign_time.points_as_df()
        points_df += game_service.reign_time.points_as_df()
        points_df.loc["C"] += gs.POINTS_FOR_LAST_KING

        assert game_service.points_df().equals(points_df)


class TestTotalReignTimeStat:
    def test_plot(self, game_service):
        assert type(game_service.total_reign_time.plot()) == mpl.figure.Figure

    def test_points(self, game_service):
        points = {
            "A": 10,
            "B": 20,
            "C": 30,
        }

        points = {player: math.ceil(gs.ALPHA * value / 60) for player, value in points.items()}

        assert game_service.total_reign_time.points == points


class TestReignTimeStat:
    def test_plot(self, game_service):
        assert type(game_service.reign_time.plot()) == mpl.figure.Figure

    def test_points(self, game_service):
        points = {
            "A": 10,
            "B": 20,
            "C": 30,
        }

        def eval_points(seconds):
            return int(math.ceil(seconds / 60 * 100)) ** gs.SIGMA

        points = {
            player: math.ceil(gs.BETA * eval_points(value)) for player, value in points.items()
        }

        assert game_service.reign_time.points == points


class TestCrownsClaimnedStat:
    def test_plot(self, game_service):
        assert type(game_service.crowns_claimed.plot()) == mpl.figure.Figure

    def test_points(self, game_service):
        points = {
            "A": 0,
            "B": 0,
            "C": 0,
        }
        assert game_service.crowns_claimed.points == points


class TestGraphVisualizationStat:
    def test_plot(self, game_service):
        assert type(game_service.graph_visualization.plot()) == mpl.figure.Figure

    def test_points(self, game_service):
        points = {
            "A": 0,
            "B": 0,
            "C": 0,
        }
        assert game_service.graph_visualization.points == points
