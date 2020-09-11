from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from social_django.models import AbstractUserSocialAuth
from rest_framework.authtoken.models import Token

import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    steam_id = models.CharField(unique=True, max_length=100, db_index=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def token(self):
        # This will sometimes be called before a token has been generated and as all users should have a token
        # one will be generated if it doesn't exist.
        return Token.objects.get_or_create(user=self)[0].key
        

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        # Create API token for every user by default
        Token.objects.create(user=instance)
