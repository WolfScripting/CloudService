from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status

from ticket.models import Ticket
from ticket.serializer import TicketSerializer
from user.serializers import UserSerializer

from django.core.validators import validate_ipv46_address



@api_view(['POST'])
def validate(request):
    secret      = request.POST['ticket']
    steam_id    = request.POST['steam_id']
    request_ip  = request.META['HTTP_X_FORWARDED_FOR']

    try:
        ticket = Ticket.objects.get(
            secret=secret,
            user__steam_id=steam_id,
            server=request_ip
        )

        if not ticket.is_valid():
            # the ticket was not valid but we don't
            # want to give away too much info so we just
            # throw a generic error to trigger the except block
            raise ValueError

    except:
        content = {'error': 'ticket_not_found'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(ticket.user)

    ticket.delete() # ticket is one-time use, delete straight away
    
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate(request):
    server_ip   = request.POST['server']
    user        = request.user

    try:
        validate_ipv46_address(server_ip) # ensure a value is either a valid IPv4 or IPv6 address
    except:
        content = {'error': 'malformed_ip'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


    ticket = Ticket.objects.create(
        user=user,
        server=server_ip
    )

    serializer = TicketSerializer(ticket)

    return Response(serializer.data, status=status.HTTP_201_CREATED)


    
