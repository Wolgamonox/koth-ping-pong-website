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
ALPHA = 190
BETA = 0.05
SIGMA = 1.9

POINTS_FOR_LAST_KING = 30


class KothStatService:
    """Wrapper class to contain all stats for the KOTH."""

    def __init__(self, players: list[str], transitions_df: pd.DataFrame):
        self.players = players
        self.transitions_df = transitions_df

        self.total_reign_time = TotalReignTimeStat(players, transitions_df)
        self.reign_time = ReignTimeStat(players, transitions_df)
        self.crowns_claimed = CrownsClaimedStat(players, transitions_df)
        self.graph_visualization = GraphVisualizationStat(players, transitions_df)

    @property
    def points_df(self):
        points_df = self.total_reign_time.points_as_df()
        points_df += self.reign_time.points_as_df()
        points_df += self.crowns_claimed.points_as_df()

        # points for being last king
        last_king = self.transitions_df.iloc[-1]["Name"]
        points_df.loc[last_king] += POINTS_FOR_LAST_KING

        return points_df


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

    def calculate_points(self, player: str) -> int:
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

    def calculate_points(self, player: str) -> int:
        def reign_time_points_eval(seconds, sigma=SIGMA):
            seconds_normalized = int(math.ceil(seconds / self.game_duration * 100))
            return seconds_normalized**sigma

        df_points = self.transitions_df.query("Name == @player").copy()

        df_points["Points"] = df_points["Duration"].apply(
            lambda seconds: reign_time_points_eval(seconds)
        )

        return math.ceil(BETA * df_points["Points"].sum())


class CrownsClaimedStat(KothStat):
    def __init__(self, players: list[str], transitions_df: pd.DataFrame):
        super().__init__(players, transitions_df)

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
    def __init__(self, players: list[str], transitions_df: pd.DataFrame):
        super().__init__(players, transitions_df)

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
