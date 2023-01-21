from django.urls import path

from .views import (
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventListView,
    EventUpdateView,
)

app_name = 'events'
urlpatterns = [
    path('', EventListView.as_view(), name='list'),
    path('<int:pk>/', EventDetailView.as_view(), name='detail'),
    path('create/', EventCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', EventDeleteView.as_view(), name='delete'),
    path('update/<int:pk>/', EventUpdateView.as_view(), name='update'),
]
