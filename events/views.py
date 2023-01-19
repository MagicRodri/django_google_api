import datetime

from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .forms import EventForm
from .models import Event

CALENDAR_API_NAME = settings.CALENDAR_API_NAME
CALENDAR_API_VERSION = settings.CALENDAR_API_VERSION


def events_list(request):
    if 'credentials' not in request.session:
        return redirect('accounts:google_auth')

    credentials = Credentials(**request.session['credentials'])

    calendar = build(CALENDAR_API_NAME,
                     CALENDAR_API_VERSION,
                     credentials=credentials)
    try:
        events_result = calendar.calendarList().list().execute()
        events = events_result.get('items', [])
    except HttpError as e:
        raise e

    return render(request,
                  'events/events_list.html',
                  context={'events': events})


class EventCreateView(CreateView):
    model = Event
    template_name = 'events/events_create.html'
    form_class = EventForm
    success_url = reverse_lazy('events')

    def get(self, *args, **kwargs):
        if 'credentials' not in self.request.session:
            return redirect('accounts:google_auth')
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