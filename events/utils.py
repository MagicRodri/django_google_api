from django.conf import settings
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

CALENDAR_API_NAME = settings.CALENDAR_API_NAME
CALENDAR_API_VERSION = settings.CALENDAR_API_VERSION


def get_calendar_service(credentials):
    return build(CALENDAR_API_NAME,
                 CALENDAR_API_VERSION,
                 credentials=credentials)


def get_calendar_list(credentials):
    calendar = get_calendar_service(credentials)
    calendars = calendar.calendarList().list().execute().get('items', [])
    if not calendars:
        return []
    # Get only the id and summary of each calendar
    cleaned_calendars = [{
        'id': calendar['id'],
        'summary': calendar['summary']
    } for calendar in calendars]
    return cleaned_calendars


def get_events(credentials, calendar_id, time_min, time_max):
    calendar = get_calendar_service(credentials)
    events = calendar.events().list(calendarId=calendar_id,
                                    timeMin=time_min,
                                    timeMax=time_max).execute().get(
                                        'items', [])
    if not events:
        return []
    # Get only the id, summary, start and end of each event
    cleaned_events = [{
        'id': event['id'],
        'summary': event['summary'],
        'location': event['location'],
        'description': event['description'],
        'start': event['start'],
        'end': event['end'],
    } for event in events]
    return cleaned_events