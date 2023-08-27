from rest_framework import serializers

from .models import Game


class GameSerializer(serializers.ModelSerializer):
    transitions = serializers.ListField(allow_empty=False)

    class Meta:
        model = Game
        fields = ["players", "transitions", "date"]

    def validate(self, data):
        """
        Verify if the players in the transitions match the players of the game.
        """
        players_pks = {player.pk for player in data["players"]}

        for transition in data["transitions"]:
            if transition["player"] not in players_pks:
                raise serializers.ValidationError(f"Invalid player in transitions. pk={transition['player']}")

        return data
