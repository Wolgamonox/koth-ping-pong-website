from rest_framework import serializers

from .models import Game


class GameSerializer(serializers.ModelSerializer):
    transitions = serializers.ListField(allow_empty=False)

    class Meta:
        model = Game
        fields = ["players", "transitions", "date"]
