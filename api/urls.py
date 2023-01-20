from django.urls import path

from .views import CalendarListAPIView, EventListAPIView, UserListAPIView

app_name = 'api'
urlpatterns = [
    path('calendars/', CalendarListAPIView.as_view(), name='calendars'),
    path('events/', EventListAPIView.as_view(), name='events'),
    path('users/', UserListAPIView.as_view(), name='users'),
]
