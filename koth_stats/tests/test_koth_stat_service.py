import math

import matplotlib as mpl
import pandas as pd
import pytest

import koth_stats.stats as ks


@pytest.fixture
def koth_service():
    players = ["A", "B", "C"]

    transitions_df = pd.DataFrame(
        {
            "Name": players,
            "Duration": [10, 20, 30],
        }
    )

    return ks.KothStatService(players, transitions_df)


class TestKothservice:
    def test_initialization(self, koth_service):
        assert koth_service.players[0] == "A"

    def test_points(self, koth_service: ks.KothStatService):
        points_df = pd.DataFrame(
            index=["A", "B", "C"],
            data={"Points": [0, 0, 0]},
        )

        points_df += koth_service.total_reign_time.points_as_df()
        points_df += koth_service.reign_time.points_as_df()
        points_df.loc["C"] += ks.POINTS_FOR_LAST_KING

        assert koth_service.points_df().equals(points_df)


class TestTotalReignTimeStat:
    def test_plot(self, koth_service):
        assert type(koth_service.total_reign_time.plot()) == mpl.figure.Figure

    def test_points(self, koth_service):
        points = {
            "A": 10,
            "B": 20,
            "C": 30,
        }

        points = {player: math.ceil(ks.ALPHA * value / 60) for player, value in points.items()}

        assert koth_service.total_reign_time.points == points


class TestReignTimeStat:
    def test_plot(self, koth_service):
        assert type(koth_service.reign_time.plot()) == mpl.figure.Figure

    def test_points(self, koth_service):
        points = {
            "A": 10,
            "B": 20,
            "C": 30,
        }

        def eval_points(seconds):
            return int(math.ceil(seconds / 60 * 100)) ** ks.SIGMA

        points = {
            player: math.ceil(ks.BETA * eval_points(value)) for player, value in points.items()
        }

        assert koth_service.reign_time.points == points


class TestCrownsClaimnedStat:
    def test_plot(self, koth_service):
        assert type(koth_service.crowns_claimed.plot()) == mpl.figure.Figure

    def test_points(self, koth_service):
        points = {
            "A": 0,
            "B": 0,
            "C": 0,
        }
        assert koth_service.crowns_claimed.points == points


class TestGraphVisualizationStat:
    def test_plot(self, koth_service):
        assert type(koth_service.graph_visualization.plot()) == mpl.figure.Figure

    def test_points(self, koth_service):
        points = {
            "A": 0,
            "B": 0,
            "C": 0,
        }
        assert koth_service.graph_visualization.points == points
