from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from .models import Game


class GameFilter(filters.FilterSet):
    # Conjoined = True means only games where all specified players are present
    players = filters.ModelMultipleChoiceFilter(
        queryset=get_user_model().objects.filter(),
        conjoined=True,
    )
    date = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Game
        fields = ["players", "date"]
