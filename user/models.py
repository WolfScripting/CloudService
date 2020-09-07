from django.contrib.auth.models import AbstractUser
from django.db import models

from allauth.socialaccount.models import SocialAccount

import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.id)
    
    @property
    def steam_account(self):
        return SocialAccount.objects.get(user=self)

    @property
    def steam_id(self):
        return self.steam_account.extra_data['steamid']