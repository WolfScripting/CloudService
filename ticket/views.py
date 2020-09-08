from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from ticket.models import Ticket
from user.serializers import UserSerializer


@csrf_exempt
@require_POST
def validate(request):
    try:
        t = Ticket.objects.get(secret=request.POST["ticket"])
        if t.user.steam_id != request.POST["steam_id"]:
            raise Ticket.DoesNotExist
        elif not t.is_valid:
            t.delete()
            raise Ticket.DoesNotExist
    except Ticket.DoesNotExist:
        return HttpResponse('404', status=404)
    except KeyError:
        return HttpResponse('400', status=400)
    else:
        serializer = UserSerializer(t.user)
        t.delete()
        return JsonResponse(serializer.data, status=200)
