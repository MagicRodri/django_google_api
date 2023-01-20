from django.urls import path

from .views import CalendarListView, EventCreateView, EventListView

app_name = 'events'
urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('calendars/', CalendarListView.as_view(), name='calendars'),
    path('create/', EventCreateView.as_view(), name='create')
]
