import datetime

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calendar_id = models.CharField(max_length=255)
    summary = models.CharField(max_length=255, blank=True)

    def __str__(self):
        if self.summary:
            return self.summary
        return self.user


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    summary = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    start = models.DateTimeField(default=datetime.datetime.utcnow() +
                                 datetime.timedelta(days=1))
    end = models.DateTimeField(default=datetime.datetime.utcnow() +
                               datetime.timedelta(days=2))
    attendees = models.ManyToManyField(User, related_name='attendees')

    def __str__(self):
        return self.summary