from django.urls import path

from .views import CalendarListView, EventCreateView, EventListView

app_name = 'events'
urlpatterns = [
    path('calendars/', CalendarListView.as_view(), name='calendars'),
    path('create/', EventCreateView.as_view(), name='create'),
    path('', EventListView.as_view(), name='list'),
]
