from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView
from rest_framework.parsers import JSONParser

from .models import Game
from .serializers import GameSerializer


class AllGamesView(ListView):
    model = Game
    template_name = "games/all_games.html"
    context_object_name = "games"


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
