from django.contrib import admin
from django.urls import include, path

from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls', namespace='api')),
    path('events/', include('events.urls', namespace='events')),
]
