from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from google.oauth2.credentials import Credentials

from accounts.utils import (
    GoogleCalendarAuthorizationRequiredMixin,
    calendar_authorization_required,
)

from .filters import EventFilter
from .forms import EventForm
from .models import Calendar, Event
from .utils import get_calendar_service, get_events

CALENDAR_API_NAME = settings.CALENDAR_API_NAME
CALENDAR_API_VERSION = settings.CALENDAR_API_VERSION


class EventListView(LoginRequiredMixin,
                    GoogleCalendarAuthorizationRequiredMixin, ListView):
    model = Event
    template_name = 'events/events_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        """Add the filter to the context.
           Refresh the events from the API if the user requested it and save to the DB.
        """
        context = super().get_context_data(**kwargs)
        filter = EventFilter(self.request.GET)
        if filter.is_valid():
            context['filter'] = filter
            fetch_from_api = self.request.GET.get("from_api")
            if fetch_from_api:
                lookup = {
                    'time_min': filter.data.get('start'),
                    'time_max': filter.data.get('end'),
                }
                credentials = Credentials(
                    **self.request.session['credentials'])
                calendar = self.request.GET.get('calendar')
                if calendar:
                    calendar = Calendar.objects.get(id=calendar)
                    lookup['calendar_id'] = calendar.calendar_id
                    events = get_events(credentials, **lookup)
                    Event.from_events_list(self.request.user, calendar, events)
                else:
                    calendars = Calendar.objects.filter(user=self.request.user)
                    for calendar in calendars:
                        lookup['calendar_id'] = calendar.calendar_id
                        events = get_events(credentials, **lookup)
                        Event.from_events_list(self.request.user, calendar,
                                               events)
        return context

    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)


class EventCreateView(LoginRequiredMixin,
                      GoogleCalendarAuthorizationRequiredMixin, CreateView):
    model = Event
    template_name = 'events/events_create.html'
    form_class = EventForm
    success_url = reverse_lazy('events:list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        event = form.save(commit=False)
        event.user = self.request.user
        event_body = {
            'summary': event.summary,
            'location': event.location,
            'description': event.description,
            'start': {
                'dateTime': event.start.isoformat(),
            },
            'end': {
                'dateTime': event.end.isoformat(),
            }
        }
        calendar_id = 'primary'
        if event.calendar:
            calendar_id = event.calendar.calendar_id
        credentials = Credentials(**self.request.session['credentials'])
        calendar = get_calendar_service(credentials)
        event = calendar.events().insert(calendarId=calendar_id,
                                         body=event_body).execute()
        return super().form_valid(form)


class CalendarListView(LoginRequiredMixin,
                       GoogleCalendarAuthorizationRequiredMixin, ListView):
    model = Calendar
    template_name = 'events/calendar_list.html'
    context_object_name = 'calendars'

    def get_queryset(self):
        return Calendar.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context