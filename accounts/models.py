from django.contrib.auth.models import AbstractUser
from django.db import models
from google.oauth2.credentials import Credentials


class User(AbstractUser):
    # add additional fields in here
    google_id = models.CharField(max_length=255,
                                 blank=True,
                                 null=True,
                                 unique=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        if self.email:
            return self.email
        return self.id


class GoogleCredential(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    scopes = models.CharField(max_length=255)

    def __str__(self):
        return self.user

    def to_dict(self):
        return {
            'token': self.token,
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'scopes': self.scopes.split(','),
        }

    def to_credentials(self):
        return Credentials(**self.to_dict())