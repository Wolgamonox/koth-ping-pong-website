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


def test_initialization(koth_service):
    assert koth_service.players[0] == "A"


class TestTotalReignTimeStat:
    def test_total_reign_time_plot(self, koth_service):
        assert type(koth_service.total_reign_time.plot()) == mpl.figure.Figure

    def test_total_reign_time_points(self, koth_service):
        points = {
            "A": 10,
            "B": 20,
            "C": 30,
        }

        points = {player: math.ceil(ks.ALPHA * value / 60) for player, value in points.items()}

        assert koth_service.total_reign_time.points == points


class TestReignTimeStat:
    def test_reign_time_plot(self, koth_service):
        assert type(koth_service.reign_time.plot()) == mpl.figure.Figure

    def test_reign_time_points(self, koth_service):
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
