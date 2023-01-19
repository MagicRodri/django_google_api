from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # add additional fields in here
    google_id = models.CharField(max_length=255,
                                 blank=True,
                                 null=True,
                                 unique=True)
