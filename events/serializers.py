from rest_framework import serializers

from .models import Calendar, Event
from .validators import clean_event_data


class CalendarSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Calendar
        fields = ['user', 'summary']


class CalendarRelatedField(serializers.PrimaryKeyRelatedField):

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.context.get('request')
        return qs.filter(user=request.user)


class EventSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    calendar = CalendarRelatedField(queryset=Calendar.objects.all())

    class Meta:
        model = Event
        fields = [
            'user', 'calendar', 'summary', 'location', 'description', 'start',
            'end'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        calendar = Calendar.objects.get(pk=data.get('calendar'))
        data['calendar'] = calendar.summary
        return data

    def validate(self, data):
        return clean_event_data(data)