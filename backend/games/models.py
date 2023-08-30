import base64
import io

import matplotlib as mpl
import pandas as pd
from accounts.models import CustomUser
from django.db import models
from django.utils import timezone

import koth_stats.game_stats as gs


class Game(models.Model):
    players = models.ManyToManyField(CustomUser)
    transitions = models.JSONField()
    date = models.DateTimeField(default=timezone.now, editable=False)

    valid = models.BooleanField(default=True)

    class Meta:
        ordering = ("-date",)

    def __str__(self):
        return f"Game [{self.pk}]"

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)

        mpl.rcParams["font.size"] = 14

        players_names = [player.first_name for player in instance.players.all()]

        transitions_df = pd.DataFrame(
            {
                "Name": [
                    CustomUser.objects.get(id=transition["player"]).first_name for transition in instance.transitions
                ],
                "Duration": [transition["duration"] for transition in instance.transitions],
            }
        )

        instance.koth_service = gs.GameStatService(players_names, transitions_df)

        return instance

    def total_reign_time_plot(self):
        """
        Pie chart representing the percentage of time as king.
        """
        fig = self.koth_service.total_reign_time.plot()
        return fig_to_base64(fig)

    def reign_time_plot(self):
        """
        Box plots representing the reign time for each player.
        """
        fig = self.koth_service.reign_time.plot()
        return fig_to_base64(fig)

    def crowns_claimed_plot(self):
        """
        Bar plot representing number of crowns claimed by each player
        """
        fig = self.koth_service.crowns_claimed.plot()
        return fig_to_base64(fig)

    def crown_transitions_plot(self):
        """
        Line plot representing transitions of the crown between each players
        """
        fig = self.koth_service.graph_visualization.plot()
        return fig_to_base64(fig)

    def points_plot(self):
        """
        Bar plot representing points for each player
        """
        fig = self.koth_service.points_plot()
        return fig_to_base64(fig)


def fig_to_base64(fig):
    """Convert matplotlib figure to base64 for html display."""

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")
