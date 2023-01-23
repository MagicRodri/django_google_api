import datetime
from typing import Union

from celery import shared_task
from django.contrib.auth import get_user_model
from google.oauth2.credentials import Credentials

from events.models import Calendar, Event
from events.utils import get_calendar_list, get_events

User = get_user_model()


@shared_task()
def get_events_from_api(user_id: int,
                        credentials_dict: dict,
                        calendar_id: str = None,
                        start: Union[str, datetime.datetime] = None,
                        end: Union[str, datetime.datetime] = None):
    """Get events from the API and save them to the DB."""

    if not user_id:
        raise ValueError("User id must be provided")
    if not credentials_dict:
        raise ValueError("Credentials must be provided")
    user = User.objects.get(id=user_id)
    credentials = Credentials(**credentials_dict)
    if calendar_id:
        calendar = Calendar.objects.get(id=calendar_id)
        lookup = {
            'time_min': start,
            'time_max': end,
            'calendar_id': calendar.calendar_id,
        }
        events = get_events(credentials, **lookup)
        Event.from_events_list(user, calendar, events)
    else:
        calendars = get_calendar_list(credentials)
        Calendar.from_calendar_list(user, calendars)
        print(calendars)
        for calendar in calendars:
            lookup = {
                'time_min': start,
                'time_max': end,
                'calendar_id': calendar['id'],
            }
            events = get_events(credentials, **lookup)
            print(events)
            calendar = Calendar.objects.get(user=user,
                                            calendar_id=calendar['id'])
            Event.from_events_list(user, calendar, events)


@shared_task
def add(x, y):
    return x + y