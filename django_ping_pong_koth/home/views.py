from django.contrib.auth.models import User
from django.http import HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home/index.html"


@require_GET
def get_player(request):
    """View to get the player information from its username"""
    query_username = request.GET.get("username", "")

    try:
        user = User.objects.get(username=query_username)
    except User.DoesNotExist:
        return HttpResponseNotFound()

    json = {
        "id": user.pk,
        "username": user.get_username(),
        "full_name": user.get_full_name(),
    }
    return JsonResponse(json)
