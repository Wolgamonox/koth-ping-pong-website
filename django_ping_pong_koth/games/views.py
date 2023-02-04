from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
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
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)


@require_GET
def get_pk_of(request):
    """View to get the primary key of user from its username"""
    query_username = request.GET.get("username", "")

    if query_username:
        return HttpResponse(User.objects.get(username=query_username).pk)
    else:
        return HttpResponseNotFound()
