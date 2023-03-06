import json
import math
from abc import ABC, abstractmethod

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
DEFAULT_ALPHA = 190
DEFAULT_BETA = 0.05
DEFAULT_SIGMA = 1.9

DEFAULT_POINTS_LAST_KING = 30

# TODO REFACTOR ALL THE SETTINGS INTO SOME SORT OF CONFIG FILE


class ScoreParameters:
    """Class holding the parameters for the score."""

    def __init__(
        self,
        alpha=DEFAULT_ALPHA,
        beta=DEFAULT_BETA,
        sigma=DEFAULT_SIGMA,
        points_last_king=DEFAULT_POINTS_LAST_KING,
    ):
        self.alpha = alpha
        self.beta = beta
        self.sigma = sigma
        self.points_last_king = points_last_king

    @classmethod
    def from_file(cls, filename: str):
        """Loads score parameters from file."""
        with open(filename, "r") as file:
            try:
                params = json.load(file)

                return ScoreParameters(
                    alpha=params["alpha"],
                    beta=params["beta"],
                    sigma=params["sigma"],
                    points_last_king=params["points_last_king"],
                )
            except Exception as e:
                print(e)

                print("Error reading config file, using default parameters instead.")
                return ScoreParameters()


class KothStatService:
    """Wrapper class to contain all stats for the KOTH."""

    def __init__(
        self,
        players: list[str],
        transitions_df: pd.DataFrame,
        score_parameters=ScoreParameters(),
    ):
        self.players = players
        self.transitions_df = transitions_df

        self.total_reign_time = TotalReignTimeStat(players, transitions_df)
        self.reign_time = ReignTimeStat(players, transitions_df)
        self.crowns_claimed = CrownsClaimedStat(players, transitions_df)
        self.graph_visualization = GraphVisualizationStat(players, transitions_df)

        self.score_parameters = score_parameters

    def points_df(self, ascending=False):
        points_df = self.total_reign_time.points_as_df()
        points_df += self.reign_time.points_as_df()
        points_df += self.crowns_claimed.points_as_df()

        # points for being last king
        last_king = self.transitions_df.iloc[-1]["Name"]
        points_df.loc[last_king] += self.score_parameters.points_last_king

        points_df = points_df.sort_values("Points", ascending=ascending)

        return points_df

    def points_plot(self, include_title=False) -> Figure:
        fig = Figure(linewidth=PLOT_LINEWIDTH)
        ax = fig.subplots()

        medal_colors_palette = sns.color_palette(
            ["#FFD700", "#C9C0BB", "#CD7F32"] + (len(self.players) - 3) * ["#3E3E40"]
        )

        points_df = self.points_df()

        sns.barplot(x=points_df.index, y=points_df.Points, palette=medal_colors_palette, ax=ax)
        ax.set_ylim([0, points_df.Points.max() + points_df.Points.max() / 10])
        ax.set_xlabel("")
        ax.bar_label(ax.containers[0])

        if include_title:
            ax.set_title("Final score")

        return fig


class KothStat(ABC):
    @abstractmethod
    def __init__(
        self,
        players: list[str],
        transitions_df: pd.DataFrame,
        score_parameters: ScoreParameters,
    ):
        self.players = players
        self.transitions_df = transitions_df
        self.score_parameters = score_parameters

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
    def calculate_points(self, player: str) -> int:
        return 0

    @property
    def points(self) -> dict[str, int]:
        return {player: self.calculate_points(player) for player in self.players}

    def points_as_df(self) -> pd.DataFrame:
        points_df = pd.DataFrame(
            {
                "Name": self.players,
                "Points": [self.calculate_points(player) for player in self.players],
            }
        )

        points_df.set_index("Name", inplace=True)

        return points_df


class TotalReignTimeStat(KothStat):
    """Class representing the total time as a king."""

    def __init__(
        self,
        players: list[str],
        transitions_df: pd.DataFrame,
        score_parameters: ScoreParameters,
    ):
        super().__init__(players, transitions_df, score_parameters)

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

    def plot(self, include_title=False) -> Figure:
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

    def calculate_points(self, player: str) -> int:
        points = self.total_reign_time_df.loc[player]["Duration"] / self.game_duration
        return math.ceil(self.score_parameters.alpha * points)


class ReignTimeStat(KothStat):
    """Class representing the reign time distribution."""

    def __init__(
        self,
        players: list[str],
        transitions_df: pd.DataFrame,
        score_parameters: ScoreParameters,
    ):
        super().__init__(players, transitions_df, score_parameters)

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

    def calculate_points(self, player: str) -> int:
        def reign_time_points_eval(seconds):
            sigma = self.score_parameters.sigma
            seconds_normalized = int(math.ceil(seconds / self.game_duration * 100))

            return seconds_normalized**sigma

        df_points = self.transitions_df.query("Name == @player").copy()

        df_points["Points"] = df_points["Duration"].apply(
            lambda seconds: reign_time_points_eval(seconds)
        )

        return math.ceil(self.score_parameters.beta * df_points["Points"].sum())


class CrownsClaimedStat(KothStat):
    """Class representing the crowns claimed."""

    def __init__(
        self,
        players: list[str],
        transitions_df: pd.DataFrame,
        score_parameters: ScoreParameters,
    ):
        super().__init__(players, transitions_df, score_parameters)

        first_king = self.transitions_df.iloc[0]["Name"]

        self.crowns_claimed_df = (
            self.transitions_df.groupby("Name")
            .count()
            .rename({"Duration": "Claimed"}, axis=1)
            .sort_values("Claimed", ascending=False)
        )

        # Substract one crown to the first king since he did not claim it
        self.crowns_claimed_df.loc[first_king]["Claimed"] -= 1

        # In case one or more player(s) were not king at all
        # Include their names in the graph still with a 0 duration
        if len(self.crowns_claimed_df) < len(self.players):
            for player in self.players:
                if player not in self.crowns_claimed_df.index:
                    self.crowns_claimed_df = pd.concat(
                        [
                            self.crowns_claimed_df,
                            pd.DataFrame({"Claimed": 0}, index=[player]),
                        ]
                    )

    def plot(self, include_title=False) -> Figure:
        fig = Figure()
        ax = fig.subplots()

        sns.barplot(
            x=self.crowns_claimed_df.index,
            y=self.crowns_claimed_df["Claimed"],
            palette=self.player_colors,
            ax=ax,
        )
        ax.set_yticks(
            range(
                0,
                int(math.ceil(self.crowns_claimed_df["Claimed"].max())) + 1,
            )
        )
        ax.set_xlabel("")
        ax.set_ylabel("")

        if include_title:
            ax.set_title("Number of crowns claimed")

        return fig

    def calculate_points(self, player: str) -> int:
        return super().calculate_points(player)


class GraphVisualizationStat(KothStat):
    """Class representing graph visualization of the crown transitions."""

    def __init__(
        self,
        players: list[str],
        transitions_df: pd.DataFrame,
        score_parameters: ScoreParameters,
    ):
        super().__init__(players, transitions_df, score_parameters)

        # normalize seconds for nice display
        transitions_df["Duration_perc"] = self.transitions_df["Duration"].apply(
            lambda seconds: int(math.ceil(seconds / self.game_duration * 100))
        )

        self.graph_vector = []
        for _, transition in transitions_df.iterrows():
            self.graph_vector.extend(transition["Name"] for _ in range(transition["Duration_perc"]))

    def plot(self, include_title=False) -> Figure:
        fig = Figure(figsize=(15, 5))
        ax = fig.subplots()

        sns.lineplot(
            x=range(len(self.graph_vector)),
            y=self.graph_vector,
            drawstyle="steps",
            ax=ax,
        )
        ax.set_xlabel("Game advancement (%)")

        if include_title:
            ax.set_title("Visualization of crown transitions")

        return fig

    def calculate_points(self, player: str) -> int:
        return super().calculate_points(player)
