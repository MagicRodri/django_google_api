from django.urls import path

from .views import EventCreateView, EventListView

app_name = 'events'
urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('create/', EventCreateView.as_view(), name='create')
]
