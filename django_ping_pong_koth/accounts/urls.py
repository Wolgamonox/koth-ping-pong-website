from django.urls import path

from .views import ProfilePageView, SignUpView

app_name = "accounts"
urlpatterns = [
    path("profile/", ProfilePageView.as_view(), name="profile"),
    path("signup/", SignUpView.as_view(), name="signup"),
]
