import django_filters
from django import forms
from django_filters.rest_framework import DjangoFilterBackend

from .models import Calendar, Event


def user_calendars(request):
    return Calendar.objects.filter(user=request.user)


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
        queryset=user_calendars,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Event
        fields = ['start', 'end', 'calendar']

    @property
    def qs(self):
        parent = super().qs
        return parent.filter(user=self.request.user)


class EventFilterBackend(DjangoFilterBackend):

    def get_filterset_class(self, view, queryset=None):
        return EventFilter

    def get_filterset_kwargs(self, request, queryset, view):
        return {
            'data': request.query_params,
            'request': request,
        }