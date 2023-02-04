import base64
import io
import urllib

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from django.contrib.auth.models import User
from django.db import models


class Game(models.Model):
    players = models.ManyToManyField(User)
    transitions = models.JSONField()
    date = models.DateTimeField(auto_now_add=True, editable=False)

    valid = models.BooleanField(default=True)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return "Game %s" % self.date.strftime("%Y-%m-%d %H:%M:%S")

    def preprocessing_df(self):
        self.transisitons_df = pd.DataFrame(
            {
                "Name": [
                    User.objects.get(id=transition["player"]).get_full_name()
                    for transition in self.transitions
                ],
                "Duration": [transition["duration"] for transition in self.transitions],
            }
        )

        self.player_colors = {
            player.get_full_name(): color
            for player, color in zip(
                self.players.all(), sns.color_palette("Pastel1", n_colors=len(self.players.all()))
            )
        }

    def get_plot_total_time(self):
        self.preprocessing_df()

        total_time_king = (
            self.transisitons_df.groupby("Name").sum().sort_values("Duration", ascending=False)
        )

        # include other players
        if len(total_time_king) < len(self.players.all()):
            for player in self.players:
                if player.get_full_name() not in total_time_king.index:
                    total_time_king = pd.concat(
                        [
                            total_time_king,
                            pd.DataFrame({"Duration": 0}, index=[player.get_full_name()]),
                        ]
                    )
        print(total_time_king)

        plt.pie(total_time_king["Duration"], labels=total_time_king.index, autopct="%.0f%%")
        pie_wedges = plt.pie(
            total_time_king["Duration"], labels=total_time_king.index, autopct="%.0f%%"
        )
        for pie_wedge in pie_wedges[0]:
            pie_wedge.set_edgecolor("white")
            pie_wedge.set_facecolor(self.player_colors[pie_wedge.get_label()])
        plt.title("Fraction of time as king")

        fig = plt.gcf()

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)

        return uri
