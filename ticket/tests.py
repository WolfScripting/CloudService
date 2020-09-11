from django.test import TestCase
from rest_framework.test import APIClient 

from user.models import User

import random
import json

class TicketTestCase(TestCase):

    def create_user(self):
        return User.objects.create(
            steam_id=str(random.randint(100000, 999999)) # random 6 digit ID to mock a steam ID
        ) 
        
    def create_ticket(self, server="100.100.100.100"):
        user = self.create_user()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user.token)

        response = client.post('/v1/ticket/generate/',{
            "server": server
        })

        return response

    def test_valid_ticket_creation(self):
        response = self.create_ticket()
        self.assertEqual(201, response.status_code)
    
    def test_ticket_secret(self):
        response = self.create_ticket()
        ticket = json.loads(response.content)
        self.assertTrue(ticket['secret'])
    
    def test_ticket_server(self):
        response = self.create_ticket()
        ticket = json.loads(response.content)
        self.assertEqual(ticket['server'], '100.100.100.100')
    
    def test_invalid_server(self):
        response = self.create_ticket(server="invalid_ip")
        json_response = json.loads(response.content)
        self.assertEqual(400, response.status_code)
        self.assertEqual(json_response['error'], "malformed_ip")
        