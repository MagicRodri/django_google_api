import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save

User = get_user_model()


class Event(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    summary = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    start = models.DateTimeField(default=datetime.datetime.utcnow() +
                                 datetime.timedelta(days=1))
    end = models.DateTimeField(default=datetime.datetime.utcnow() +
                               datetime.timedelta(days=2))

    # attendees = models.CharField(max_length=255) # TODO: add attendees

    def __str__(self):
        return self.summary


def create_event(sender, instance, created, **kwargs):
    if created:
        event = {
            'summary': instance.summary,
            'location': instance.location,
            'description': instance.description,
            'start': {
                'dateTime': instance.start.isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': instance.end.isoformat(),
                'timeZone': 'America/Los_Angeles',
            }
        }