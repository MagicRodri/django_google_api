from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView

from accounts.models import User
from accounts.serializers import UserSerializer
from events.models import Calendar, Event
from events.serializers import CalendarSerializer, EventSerializer


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'email']


class EventListAPIView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'start': ['gte', 'exact'],
        'end': ['lte', 'exact'],
    }


class CalendarListAPIView(ListAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__username']
