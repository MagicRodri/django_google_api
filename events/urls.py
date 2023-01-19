from django.urls import path

from .views import EventCreateView, events_list

app_name = 'events'
urlpatterns = [
    path('create/', EventCreateView.as_view(), name='create'),
    path('', events_list, name='list'),
]
