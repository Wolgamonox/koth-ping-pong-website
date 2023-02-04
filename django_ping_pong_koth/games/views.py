from django.views.generic import ListView

from .models import Game


class AllGamesView(ListView):
    model = Game
    template_name = "games/index.html"
    context_object_name = "games"
