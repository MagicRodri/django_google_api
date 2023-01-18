from django.urls import path

from .views import EventCreateView, index

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='event_create'),
    path('', index, name='events'),
]
