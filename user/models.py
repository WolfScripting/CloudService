from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.socialaccount.models import SocialAccount
from rest_framework.authtoken.models import Token

import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    steam_id = models.CharField(unique=True, max_length=100, db_index=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def steam_account(self):
        return SocialAccount.objects.get(user=self)


@receiver(post_save, sender=SocialAccount)
def save_steam_id_to_user(sender, instance, created, **kwargs):
    if created:
        # Saves the Steam ID to the User model so it can be queried directly 
        instance.user.steam_id = instance.extra_data['steamid']
        instance.user.save()


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        # Create API token for every user by default
        Token.objects.create(user=instance)
