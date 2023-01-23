import datetime
from urllib.parse import quote_plus

from dateutil import parser
from django.contrib.auth import get_user_model
from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse

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
    summary = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    attendees = models.ManyToManyField(User, related_name='attendees')

    def __str__(self):
        return self.show_summary

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'pk': self.pk})

    @property
    def show_summary(self):
        if self.summary:
            return self.summary
        return "No summary"

    @property
    def show_start(self):
        if self.start:
            return self.start.strftime('%Y-%m-%d %H:%M')

    @property
    def show_end(self):
        if self.end:
            return self.end.strftime('%Y-%m-%d %H:%M')

    @property
    def show_location(self):
        if self.location:
            return self.location
        return 'No location'

    @property
    def location_is_link(self):
        validate = URLValidator()
        try:
            validate(self.location)
        except:
            return False
        return True

    @property
    def location_link(self):
        if self.location_is_link:
            return self.location
        else:
            return quote_plus(
                f"https://www.google.com/maps/place/{self.location}",
                safe=':/?=')

    @property
    def show_description(self):
        if self.description:
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