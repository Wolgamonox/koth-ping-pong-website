from django.urls import path

from . import views

app_name = "home"
urlpatterns = [
    path("", views.HomePageView.as_view(), name="homepage"),
    path("accounts/profile/", views.ProfilePageView.as_view(), name="profile"),
    path("about", views.AboutPageView.as_view(), name="about"),
    path("privacy-policy", views.PrivacyPolicyPageView.as_view(), name="privacy-policy"),
    path(
        "terms-and-conditions",
        views.TermsAndConditionsPageView.as_view(),
        name="terms-and-conditions",
    ),
    path("get-player", views.get_player),
]
