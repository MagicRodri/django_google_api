import django_filters
from django import forms

from .models import Calendar, Event


class EventFilter(django_filters.FilterSet):
    start = django_filters.DateTimeFilter(
        field_name='start',
        lookup_expr='gte',
        label='Start',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
    )

    end = django_filters.DateTimeFilter(
        field_name='end',
        lookup_expr='lte',
        label='End',
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
    )

    calendar = django_filters.ModelChoiceFilter(
        field_name='calendar',
        label='Calendar',
        queryset=Calendar.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Event
        fields = ['start', 'end', 'calendar']