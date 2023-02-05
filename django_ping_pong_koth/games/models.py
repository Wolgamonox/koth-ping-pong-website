import base64
import io
from math import ceil

import matplotlib as mpl
import pandas as pd
import seaborn as sns
from django.contrib.auth.models import User
from django.db import models
from matplotlib.figure import Figure


class Game(models.Model):
    players = models.ManyToManyField(User)
    transitions = models.JSONField()
    date = models.DateTimeField(auto_now_add=True, editable=False)

    valid = models.BooleanField(default=True)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return "Game [%d]" % self.pk

    def preprocessing_df(self):
        """
        Preprocessing the transition data into a usable dataframe.

        The dataframe contains the transitions in the format:
        Name (player name) | Duration
        """

        mpl.rcParams["font.size"] = 14

        self.transisitons_df = pd.DataFrame(
            {
                "Name": [
                    User.objects.get(id=transition["player"]).get_full_name()
                    for transition in self.transitions
                ],
                "Duration": [transition["duration"] for transition in self.transitions],
            }
        )

        # Define a set of unique colors for consistent painting for each graph
        self.player_colors = {
            player.get_full_name(): color
            for player, color in zip(
                self.players.all(), sns.color_palette("Pastel1", n_colors=len(self.players.all()))
            )
        }

    def total_time_king_plot(self):
        """
        Pie chart representing the percentage of time as king.
        """
        self.preprocessing_df()

        total_time_king = (
            self.transisitons_df.groupby("Name").sum().sort_values("Duration", ascending=False)
        )

        # In case one or more player(s) were not king at all
        # Include their names in the graph still with a 0 duration
        if len(total_time_king) < len(self.players.all()):
            for player in self.players.all():
                if player.get_full_name() not in total_time_king.index:
                    total_time_king = pd.concat(
                        [
                            total_time_king,
                            pd.DataFrame({"Duration": 0}, index=[player.get_full_name()]),
                        ]
                    )

        fig = Figure(linewidth=12)
        ax = fig.subplots()

        ax.pie(total_time_king["Duration"], labels=total_time_king.index, autopct="%.0f%%")
        pie_wedges = ax.pie(
            total_time_king["Duration"], labels=total_time_king.index, autopct="%.0f%%"
        )
        for pie_wedge in pie_wedges[0]:
            pie_wedge.set_edgecolor("white")
            pie_wedge.set_facecolor(self.player_colors[pie_wedge.get_label()])
        ax.set_title("Fraction of time as king")

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data

    def reign_time_plot(self):
        """
        Box plots representing the reign time for each player.
        """
        self.preprocessing_df()

        reign_time = self.transisitons_df

        # In case one or more player(s) were not king at all
        # Include their names in the graph still with a 0 duration
        if len(reign_time["Name"].unique()) < len(self.players.all()):
            for player in self.players.all():
                if player not in reign_time["Name"].unique():
                    reign_time = pd.concat(
                        [
                            reign_time,
                            pd.DataFrame({"Name": [player.get_full_name()], "Duration": [0]}),
                        ]
                    )

        fig = Figure()
        ax = fig.subplots()

        sns.boxplot(reign_time, x="Name", y="Duration", palette=self.player_colors, ax=ax)
        ax.set_xlabel("")
        ax.set_ylabel("Seconds")
        ax.set_title("Reign time")

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data

    def crowns_claimed_plot(self):
        """
        Bar plot representing number of crowns claimed by each player
        """
        self.preprocessing_df()

        first_king = self.transisitons_df.iloc[0]["Name"]

        crowns_claimed = (
            self.transisitons_df.groupby("Name")
            .count()
            .rename({"Duration": "Claimed"}, axis=1)
            .sort_values("Claimed", ascending=False)
        )

        # Substract 1 crown to the first king since he did not claim it
        crowns_claimed.loc[first_king]["Claimed"] -= 1

        # In case one or more player(s) were not king at all
        # Include their names in the graph still with a 0 duration
        if len(crowns_claimed) < len(self.players.all()):
            for player in self.players.all():
                if player not in crowns_claimed.index:
                    crowns_claimed = pd.concat(
                        [
                            crowns_claimed,
                            pd.DataFrame({"Claimed": 0}, index=[player.get_full_name()]),
                        ]
                    )

        fig = Figure()
        ax = fig.subplots()

        sns.barplot(
            x=crowns_claimed.index, y=crowns_claimed.Claimed, palette=self.player_colors, ax=ax
        )
        ax.set_yticks(range(0, int(ceil(crowns_claimed["Claimed"].max())) + 1))
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_title("Number of crowns claimed")

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data

    def crown_transitions_plot(self):
        """
        Line plot representing transitions of the crown between each players
        """

        self.preprocessing_df()

        total_duration_seconds = self.transisitons_df["Duration"].sum()

        self.transisitons_df["Duration_perc"] = self.transisitons_df["Duration"].apply(
            lambda x: int(ceil(x / total_duration_seconds * 100))
        )

        graph_vector = []
        for _, transition in self.transisitons_df.iterrows():
            graph_vector.extend(transition.Name for _ in range(transition.Duration_perc))

        fig = Figure(figsize=(15, 5))
        ax = fig.subplots()

        sns.lineplot(x=range(len(graph_vector)), y=graph_vector, drawstyle="steps", ax=ax)
        ax.set_xlabel("Game advancement (percent)")
        ax.set_title("Visualization of crown transitions")

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data
