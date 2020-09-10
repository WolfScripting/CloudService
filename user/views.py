from django.http import HttpResponse, JsonResponse
from user.serializers import UserSerializer


def token(request):
    try:

        return JsonResponse({**UserSerializer(request.user).data, **{"token": request.user.token}})
    except AttributeError:
        return HttpResponse(status=401)
