from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status

from ticket.models import Ticket
from ticket.serializer import TicketSerializer
from user.serializers import UserSerializer

from django.core.validators import validate_ipv46_address

import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def validate(request):
    logger = logging.getLogger('ticket.validate')

    secret      = request.POST.get('ticket')
    steam_id    = request.POST.get('steam_id')
    request_ip  = request.META.get('HTTP_X_FORWARDED_FOR')

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
        logger.info(f"Validation of ticket [{secret}] for user [{steam_id}] from [{request_ip}] failed")

        content = {'error': 'ticket_not_found'}
        return Response(content, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(ticket.user)

    ticket.delete() # ticket is one-time use, delete straight away
    
    logger.info(f"Validation of ticket [{secret}] for user [{steam_id}] from [{request_ip}] success")

    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_classes([IsAuthenticated])
def generate(request):
    server_ip   = request.POST.get('server')
    user        = request.user

    try:
        validate_ipv46_address(server_ip) # ensure a value is either a valid IPv4 or IPv6 address
    except:
        logger.info(f"Generation of ticket for user [{user.id}] for server IP [{server_ip}] failed")

        content = {'error': 'malformed_ip'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)


    ticket = Ticket.objects.create(
        user=user,
        server=server_ip
    )

    serializer = TicketSerializer(ticket)

    logger.info(f"Generation of ticket for user [{user.id}] for server IP [{server_ip}] success")

    return Response(serializer.data, status=status.HTTP_201_CREATED)


    
