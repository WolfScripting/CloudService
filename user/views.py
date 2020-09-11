from django.http import HttpResponse, JsonResponse
from user.serializers import UserSerializer

from django.shortcuts import render

def home(request):
    return render(request, 'user/home.html')

def token(request):
    try:

        return JsonResponse({**UserSerializer(request.user).data, **{"token": request.user.token}})
    except AttributeError:
        return HttpResponse(status=401)
