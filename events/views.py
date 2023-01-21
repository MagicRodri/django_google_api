from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError as GoogleHttpError

from accounts.utils import GoogleCalendarAuthorizationRequiredMixin

from .filters import EventFilter
from .forms import EventForm
from .models import Calendar, Event
from .utils import get_calendar_list, get_calendar_service, get_events

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
        filter = EventFilter(data=self.request.GET, request=self.request)
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
                calendar = filter.data.get('calendar')
                if calendar:
                    calendar = Calendar.objects.get(id=calendar)
                    lookup['calendar_id'] = calendar.calendar_id
                    events = get_events(credentials, **lookup)
                    Event.from_events_list(self.request.user, calendar, events)
                else:
                    calendars = get_calendar_list(credentials)
                    Calendar.from_calendar_list(self.request.user, calendars)
                    for calendar in calendars:
                        lookup['calendar_id'] = calendar['id']
                        events = get_events(credentials, **lookup)
                        calendar = Calendar.objects.get(
                            user=self.request.user, calendar_id=calendar['id'])
                        Event.from_events_list(self.request.user, calendar,
                                               events)
        return context


class EventDetailView(LoginRequiredMixin,
                      GoogleCalendarAuthorizationRequiredMixin, DetailView):
    """
    Display the details of an event.
    """
    model = Event
    template_name = 'events/events_detail.html'
    context_object_name = 'event'


class EventCreateView(LoginRequiredMixin,
                      GoogleCalendarAuthorizationRequiredMixin, CreateView):
    """
    Create a new event in the DB and in the Google Calendar.
    """
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
        try:
            calendar = get_calendar_service(credentials)
            event = calendar.events().insert(calendarId=calendar_id,
                                             body=event_body).execute()
        except GoogleHttpError as e:
            message = f"Error creating the event in the Google Calendar! Reason: {e._get_reason()}"
            form.add_error(None, message)
            return super().form_invalid(form)
        return super().form_valid(form)


class EventUpdateView(LoginRequiredMixin,
                      GoogleCalendarAuthorizationRequiredMixin, UpdateView):
    """
    Update an event in the DB and in the Google Calendar.
    """
    model = Event
    template_name = 'events/events_update.html'
    form_class = EventForm

    def get_success_url(self) -> str:
        return reverse_lazy('events:detail', kwargs={'pk': self.object.id})

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
        try:
            calendar = get_calendar_service(credentials)
            event = calendar.events().update(calendarId=calendar_id,
                                             eventId=event.event_id,
                                             body=event_body).execute()
        except GoogleHttpError as e:
            if e.resp.status in [404, 410, 403]:
                message = 'The event does not exist in the Google Calendar.'
            form.add_error(None, message)
            return super().form_invalid(form)
        return super().form_valid(form)


class EventDeleteView(LoginRequiredMixin,
                      GoogleCalendarAuthorizationRequiredMixin, DeleteView):
    """
    Delete an event from the DB and from the Google Calendar.
    """
    model = Event
    template_name = 'events/events_delete.html'
    success_url = reverse_lazy('events:list')
    context_object_name = 'event'

    def form_valid(self, request, *args, **kwargs):
        event = self.get_object()
        credentials = Credentials(**self.request.session['credentials'])
        try:
            calendar_service = get_calendar_service(credentials)
            calendar_service.events().delete(
                calendarId=event.calendar.calendar_id,
                eventId=event.event_id).execute()
        except GoogleHttpError as e:
            if e.resp.status in [410, 404]:
                pass
        return super().form_valid(request, *args, **kwargs)