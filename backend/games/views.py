from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from rest_framework import mixins, serializers, status, viewsets
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Game
from .serializers import GameSerializer


class GamesViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Game.objects.filter(valid=True)
    serializer_class = GameSerializer

    def create(self, request, *args, **kwargs):
        # Serializer validation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verify if players pk in the transitions match the players of that game
        players_pks = {player.pk for player in serializer.validated_data["players"]}
        transitions = serializer.validated_data["transitions"]

        for transition in transitions:
            if transition["player"] not in players_pks:
                raise serializers.ValidationError(
                    detail=f"Invalid player in transitions. pk={transition['player']}", code="does_not_exist"
                )

        # Finally create the game
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# --------------------------------------------
# OLD API TO BE DELETED
class AllGamesView(ListView):
    model = Game
    template_name = "games/all_games.html"
    context_object_name = "games"
    queryset = Game.objects.filter(valid=True)

    # Temporary hotfix to not fetch all games
    queryset = queryset[:10]


class GameDetailView(DetailView):
    model = Game
    template_name = "games/game_detail.html"
    context_object_name = "game"


@csrf_exempt
@require_POST
def upload_game(request):
    """Api endpoint view to upload a game from the mobile app."""
    data = JSONParser().parse(request)

    serializer = GameSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


def update_score_parameters(request):
    pass


# --------------------------------------------------------------
