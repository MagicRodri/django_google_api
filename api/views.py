from django_filters.rest_framework import DjangoFilterBackend
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError as GoogleHttpError
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.serializers import ValidationError

from accounts.models import User
from accounts.serializers import UserSerializer
from events.filters import EventFilterBackend
from events.models import Calendar, Event
from events.serializers import CalendarSerializer, EventSerializer
from events.utils import get_calendar_service


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'email']


class EventListAPIView(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [EventFilterBackend]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        print("Inspection:", serializer.validated_data)
        event_data = serializer.validated_data
        event_body = {
            'summary': event_data.get('summary'),
            'location': event_data.get('location'),
            'description': event_data.get('description'),
            'start': {
                'dateTime': event_data.get('start').isoformat(),
            },
            'end': {
                'dateTime': event_data.get('end').isoformat(),
            }
        }
        try:
            calendar_id = 'primary'
            if event_data.get('calendar'):
                calendar_id = event_data.get('calendar').calendar_id
            credentials = Credentials(**self.request.session['credentials'])
            calendar = get_calendar_service(credentials)
            event = calendar.events().insert(calendarId=calendar_id,
                                             body=event_body).execute()
        except GoogleHttpError as e:
            message = f"Error creating the event in the Google Calendar! Reason: {e._get_reason()}"
            raise ValidationError(message)
        except KeyError:
            raise ValidationError(
                "Your session credentials can be found.You need to logout and login again!"
            )
        serializer.save(user=self.request.user)


class CalendarListAPIView(ListAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__username']
