from dateutil import parser
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView
from google.oauth2.credentials import Credentials

from accounts.utils import (
    GoogleCalendarAuthorizationRequiredMixin,
    calendar_authorization_required,
)

from .forms import EventForm
from .models import Calendar, Event
from .utils import get_calendar_service, get_events

CALENDAR_API_NAME = settings.CALENDAR_API_NAME
CALENDAR_API_VERSION = settings.CALENDAR_API_VERSION


class EventFilterView(LoginRequiredMixin,
                      GoogleCalendarAuthorizationRequiredMixin, TemplateView):
    template_name = 'events/events_filter.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['calendars'] = Calendar.objects.filter(user=self.request.user)
        return context

    def post(self, *args, **kwargs):
        start_time = parser.parse(self.request.POST.get('start'))
        end_time = parser.parse(self.request.POST.get('end'))
        calendar = self.request.POST.get('calendar')
        credentials = Credentials(
            **self.request.user.googlecredential.to_dict())
        calendar = get_calendar_service(credentials)
        try:
            events = get_events(credentials,
                                calendar_id=calendar,
                                time_min=start_time,
                                time_max=end_time)
            for event in events:
                event, created = Event.objects.get_or_create(
                    user=self.request.user,
                    calendar=calendar,
                    summary=event.get('summary', ''),
                    location=event.get('location', ''),
                    description=event.get('description', ''),
                )
        except Exception as e:
            pass
        return self.get(self, *args, **kwargs)


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
    success_url = reverse_lazy('events:list')

    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def form_valid(self, form):
        event = form.save(commit=False)
        event.user = self.request.user
        event_body = {
            'summary': event.summary,
            'location': event.location,
            'description': event.description,
            'start': {
                'dateTime': event.start.isoformat() + 'Z',
            },
            'end': {
                'dateTime': event.end.isoformat() + 'Z',
            }
        }
        credentials = Credentials(
            **self.request.user.googlecredential.to_dict())
        calendar = get_calendar_service(credentials)
        event = calendar.events().insert(calendarId='primary',
                                         body=event_body).execute()
        return super().form_valid(form)


class CalendarListView(LoginRequiredMixin,
                       GoogleCalendarAuthorizationRequiredMixin, ListView):
    model = Calendar
    template_name = 'events/calendar_list.html'
    context_object_name = 'calendars'

    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_queryset(self):
        return Calendar.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context