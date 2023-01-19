from django.contrib import admin
from django.urls import include, path

from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('events/', include('events.urls', namespace='events')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('admin/', admin.site.urls),
]
