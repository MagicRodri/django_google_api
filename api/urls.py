from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import (
    CalendarListAPIView,
    EventDetailAPIView,
    EventListAPIView,
    UserListAPIView,
)

schema_view = get_schema_view(openapi.Info(
    title="Calendar API",
    default_version='v1',
    description="Calendar API",
    terms_of_service="https://www.google.com/policies/terms/",
    contact=openapi.Contact(email="dummy@example.com"),
    license=openapi.License(name="BSD License"),
),
                              public=True,
                              permission_classes=(permissions.AllowAny, ))

app_name = 'api'
urlpatterns = [
    path('calendars/', CalendarListAPIView.as_view(), name='calendars_list'),
    path('events/', EventListAPIView.as_view(), name='events_list'),
    path('events/<int:id>/', EventDetailAPIView.as_view(),
         name='event_detail'),
    path('users/', UserListAPIView.as_view(), name='users_list'),
    path('swagger/',
         schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/',
         schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]
