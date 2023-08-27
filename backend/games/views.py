from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.parsers import JSONParser

from .filters import GameFilter
from .models import Game
from .serializers import GameSerializer


class GamesViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Game.objects.filter(valid=True)
    serializer_class = GameSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GameFilter


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
