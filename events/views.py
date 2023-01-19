import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from accounts.utils import (
    GoogleCalendarAuthorizationRequiredMixin,
    calendar_authorization_required,
)

from .forms import EventForm
from .models import Calendar, Event

CALENDAR_API_NAME = settings.CALENDAR_API_NAME
CALENDAR_API_VERSION = settings.CALENDAR_API_VERSION


class EventListView(LoginRequiredMixin,
                    GoogleCalendarAuthorizationRequiredMixin, ListView):
    model = Event
    template_name = 'events/events_list.html'
    context_object_name = 'events'

    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)


class EventCreateView(LoginRequiredMixin,
                      GoogleCalendarAuthorizationRequiredMixin, CreateView):
    model = Event
    template_name = 'events/events_create.html'
    form_class = EventForm
    success_url = reverse_lazy('events')

    @calendar_authorization_required
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def form_valid(self, form):
        event = form.save(commit=False)
        event.creator = self.request.user
        event_body = {
            'summary': event.summary,
            'location': event.location,
            'description': event.description,
            'start': {
                'dateTime': event.start.isoformat(),
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': event.end.isoformat(),
                'timeZone': 'America/Los_Angeles',
            }
        }
        credentials = Credentials(**self.request.session['credentials'])
        calendar = build(CALENDAR_API_NAME, 'v3', credentials=credentials)
        event = calendar.events().insert(calendarId='primary',
                                         body=event_body).execute()
        return super().form_valid(form)


class CalendarListView(LoginRequiredMixin,
                       GoogleCalendarAuthorizationRequiredMixin, ListView):
    model = Calendar
    template_name = 'events/calendar_list.html'
    context_object_name = 'calendars'

    @calendar_authorization_required
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_queryset(self):
        return Calendar.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context