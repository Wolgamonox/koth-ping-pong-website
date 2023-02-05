from django.urls import path

from . import views

app_name = "games"
urlpatterns = [
    path("", views.AllGamesView.as_view(), name="all"),
    path("<int:pk>/", views.GameDetailView.as_view(), name="detail"),
    # API for mobile app
    path("upload", views.upload_game),
    path("get_pk_of", views.get_pk_of),
]
