from django.conf import settings
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


def get_events(credentials, calendar_id, time_min=None, time_max=None):
    calendar = get_calendar_service(credentials)
    lookup = {'calendarId': calendar_id}
    if time_min:
        if not isinstance(time_min, str):
            time_min = time_min.isoformat() + 'Z'
        lookup['timeMin'] = time_min
    if time_max:
        if not isinstance(time_max, str):
            time_max = time_max.isoformat() + 'Z'
        lookup['timeMax'] = time_max

    events = calendar.events().list(**lookup).execute().get('items', [])
    if not events:
        return []
    # Get only the id, summary, start and end of each event
    cleaned_events = [{
        'id': event['id'],
        'summary': event['summary'],
        'location': event.get('location', ''),
        'description': event.get('description', ''),
        'start': event.get('start', {}).get('dateTime', ''),
        'end': event.get('end', {}).get('dateTime', '')
    } for event in events]
    return cleaned_events