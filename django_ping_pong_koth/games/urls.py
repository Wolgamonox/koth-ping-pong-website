from django.urls import path

from . import views

urlpatterns = [
    path("", views.AllGamesView.as_view(), name="all-games"),
    path("<int:pk>/", views.GameDetailView.as_view(), name="game-detail"),
    path("upload", views.upload_game),
    path("get_pk_of", views.get_pk_of),
]
