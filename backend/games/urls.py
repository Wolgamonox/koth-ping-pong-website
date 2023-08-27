from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("all", views.GamesViewSet)

app_name = "games"
urlpatterns = [
    path("", views.AllGamesView.as_view(), name="all"),
    path("<int:pk>/", views.GameDetailView.as_view(), name="detail"),
    path("upload", views.upload_game),  # API for mobile app
] + router.urls
