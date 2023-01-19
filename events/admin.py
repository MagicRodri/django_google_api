from django.contrib import admin

from .models import Calendar, Event

# Register your models here.

admin.site.register(Event)
admin.site.register(Calendar)
