from rest_framework import serializers

from .models import Calendar, Event


class CalendarSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Calendar
        fields = ['user', 'summary']


class EventSerializer(serializers.ModelSerializer):
    calendar = CalendarSerializer()

    class Meta:
        model = Event
        fields = [
            'calendar', 'summary', 'location', 'description', 'start', 'end'
        ]