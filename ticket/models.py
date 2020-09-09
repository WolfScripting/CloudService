from django.db import models
from user.models import User

from django.utils import timezone

from functools import partial

import datetime
import secrets


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(default=timezone.now() + datetime.timedelta(minutes=5))

    secret = models.CharField(default=partial(secrets.token_urlsafe, 32), max_length=100)

    def __str__(self):
        return self.secret

    @property
    def is_valid(self):
        return timezone.now() <= self.expiry

    @property
    def steam_id(self):
        return self.user.steam_id
