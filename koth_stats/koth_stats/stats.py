import math
from abc import ABC, abstractmethod

# import matplotlib as mpl
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure

# transitions_df format is the following:

#     Name    Duration
# 0   Bob     64
# 1   Alice   20
# 2   John    32
# 3   Bob     35

# PLOTS SETTINGS
PLOT_LINEWIDTH = 12

# DEFAULT POINTS SETTINGS
ALPHA = 100
BETA = 0.05
SIGMA = 1.9


class KothStatService:
    """Wrapper class to contain all stats for the KOTH."""

    def __init__(self, players: list[str], transitions_df: pd.DataFrame):
        self.players = players
        self.total_reign_time = TotalReignTimeStat(players, transitions_df)
        self.reign_time = ReignTimeStat(players, transitions_df)


class KothStat(ABC):
    @abstractmethod
    def __init__(self, players: list[str], transitions_df: pd.DataFrame):
        self.players = players
        self.transitions_df = transitions_df

        self.game_duration = transitions_df["Duration"].sum()

        # Define a set of unique colors for consistent painting for each graph
        self.player_colors = {
            player: color
            for player, color in zip(
                players,
                sns.color_palette("Pastel1", n_colors=len(players)),
            )
        }

    @abstractmethod
    def plot(self, include_title=False) -> Figure:
        pass

    @abstractmethod
    def calculate_points(self, player: str) -> float:
        return 0

    @property
    def points(self) -> dict[str, float]:
        return {player: self.calculate_points(player) for player in self.players}


class TotalReignTimeStat(KothStat):
    """Class representing the total time as a king"""

    def __init__(self, players: list[str], transitions_df: pd.DataFrame):
        super().__init__(players, transitions_df)

        self.total_reign_time_df = self.transitions_df.groupby("Name").sum()
        self.total_reign_time_df.sort_values("Duration", ascending=False)

        # In case one or more player(s) were not king at all
        # Include their names in the graph still with a 0 duration
        if len(self.total_reign_time_df) < len(self.players):
            for player in self.players:
                if player not in self.total_reign_time_df.index:
                    self.total_reign_time_df = pd.concat(
                        [
                            self.total_reign_time_df,
                            pd.DataFrame({"Duration": 0}, index=[player]),
                        ]
                    )

    def plot(self, include_title=True) -> Figure:
        fig = Figure(linewidth=PLOT_LINEWIDTH)
        ax = fig.subplots()

        pie_wedges = ax.pie(
            self.total_reign_time_df["Duration"],
            labels=self.total_reign_time_df.index,
            autopct="%.0f%%",
        )
        for pie_wedge in pie_wedges[0]:
            pie_wedge.set_edgecolor("white")
            pie_wedge.set_facecolor(self.player_colors[pie_wedge.get_label()])

        if include_title:
            ax.set_title("Fraction of time as king")

        return fig

    def calculate_points(self, player: str) -> float:
        points = self.total_reign_time_df.loc[player]["Duration"] / self.game_duration
        return math.ceil(ALPHA * points)


class ReignTimeStat(KothStat):
    """Class representing the reign time distribution"""

    def __init__(self, players: list[str], transitions_df: pd.DataFrame):
        super().__init__(players, transitions_df)

        # In case one or more player(s) were not king at all
        # Include their names in the graph still with a 0 duration
        if len(self.transitions_df["Name"].unique()) < len(self.players):
            for player in self.players:
                if player not in self.transitions_df["Name"].unique():
                    self.transitions_df = pd.concat(
                        [
                            self.transitions_df,
                            pd.DataFrame({"Name": [player], "Duration": [0]}),
                        ]
                    )

    def plot(self, include_title=False) -> Figure:
        fig = Figure()
        ax = fig.subplots()

        sns.boxplot(self.transitions_df, x="Name", y="Duration", palette=self.player_colors, ax=ax)
        ax.set_xlabel("")
        ax.set_ylabel("Seconds")

        if include_title:
            ax.set_title("Reign time")

        return fig

    def calculate_points(self, player: str) -> float:
        def reign_time_points_eval(seconds, sigma=SIGMA):
            seconds_normalized = int(math.ceil(seconds / self.game_duration * 100))
            return seconds_normalized**sigma

        df_points = self.transitions_df.query("Name == @player").copy()

        df_points["Points"] = df_points["Duration"].apply(
            lambda seconds: reign_time_points_eval(seconds)
        )

        return math.ceil(BETA * df_points["Points"].sum())
