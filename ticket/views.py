from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from ticket.models import Ticket
from ticket.serializer import TicketSerializer

from user.serializers import UserSerializer


@api_view(['POST'])
def validate(request):
    try:
        t = Ticket.objects.get(secret=request.POST['ticket'])
        if t.user.steam_id != request.POST['steam_id']:
            # This should only be caused if the server provides an incorrect steam id.
            # As this could be an attack vector for invalidating tickets without them being used,
            # It should NOT be deleted and instead act as if it doesn't exist at all.
            raise Ticket.DoesNotExist
        elif t.server != request.META['HTTP_X_FORWARDED_FOR']:
            return Response(status=401)
        elif not t.is_valid:
            t.delete()
            raise Ticket.DoesNotExist
    except Ticket.DoesNotExist:
        return Response(status=404)
    except KeyError:
        return Response(status=400)
    else:
        serializer = UserSerializer(t.user)
        t.delete()
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate(request):
    try:
        ticket = Ticket.objects.create(user=request.user, server=request.POST['server'])
    except KeyError:
        return Response(status=400)
    return Response(TicketSerializer(ticket).data)
