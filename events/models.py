import datetime

from dateutil import parser
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

    @classmethod
    def from_calendar_list(cls, user, calendars):
        for calendar in calendars:
            defaults = {
                'summary': calendar.get('summary', ''),
            }
            cls.objects.update_or_create(user=user,
                                         calendar_id=calendar['id'],
                                         defaults=defaults)


def default_start():
    return datetime.datetime.utcnow() + datetime.timedelta(days=1)


def default_end():
    return datetime.datetime.utcnow() + datetime.timedelta(days=2)


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    event_id = models.CharField(max_length=255, blank=True)
    summary = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    start = models.DateTimeField(default=default_start)
    end = models.DateTimeField(default=default_end)
    attendees = models.ManyToManyField(User, related_name='attendees')

    def __str__(self):
        return self.summary

    @property
    def show_start(self):
        return self.start.strftime('%Y-%m-%d %H:%M')

    @property
    def show_end(self):
        return self.end.strftime('%Y-%m-%d %H:%M')

    @property
    def show_location(self):
        if self.location:
            if len(self.location) > 20:
                return self.location[:20] + '...'
        return 'No location'

    @property
    def show_description(self):
        if self.description:
            if len(self.description) > 100:
                return self.description[:100] + '...'
            return self.description
        return 'No description'

    @classmethod
    def from_events_list(cls, user, calendar, events):
        for event in events:
            defaults = {
                'calendar': calendar,
                'summary': event.get('summary', ''),
                'location': event.get('location', ''),
                'description': event.get('description', ''),
            }
            start = event.get('start')
            if start:
                start = parser.parse(start)
                defaults['start'] = start
            end = event.get('end')
            if end:
                end = parser.parse(end)
                defaults['end'] = end

            cls.objects.update_or_create(
                user=user,
                event_id=event.get('id', ''),
                defaults=defaults,
            )