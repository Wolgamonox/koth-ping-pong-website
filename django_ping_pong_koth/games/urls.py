from django.urls import path

from . import views

urlpatterns = [
    path("", views.AllGamesView.as_view(), name="all_games"),
]
