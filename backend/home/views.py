from accounts.models import CustomUser
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home/homepage.html"


class AboutPageView(TemplateView):
    template_name = "home/about.html"


class PrivacyPolicyPageView(TemplateView):
    template_name = "home/privacy_policy.html"


class TermsAndConditionsPageView(TemplateView):
    template_name = "home/terms_and_conditions.html"


@require_GET
def get_player(request):
    """View to get the player information from its username"""
    query_username = request.GET.get("username", "")

    try:
        user = CustomUser.objects.get(username=query_username)
    except CustomUser.DoesNotExist:
        return HttpResponseNotFound()

    json = {
        "id": user.pk,
        "username": user.get_username(),
        "full_name": user.get_full_name(),
    }
    return JsonResponse(json)
