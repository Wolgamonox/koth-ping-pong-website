from django.urls import path

from . import views

app_name = "home"
urlpatterns = [
    path("get_player", views.get_player),
]
