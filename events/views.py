import datetime

from django.shortcuts import redirect, render
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def index(request):
    if 'credentials' not in request.session:
        return redirect('google_auth')

    credentials = Credentials(**request.session['credentials'])

    calendar = build('calendar', 'v3', credentials=credentials)
    try:
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat(
        ) + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = calendar.events().list(calendarId='primary',
                                               timeMin=now,
                                               maxResults=10,
                                               singleEvents=True,
                                               orderBy='startTime').execute()
        events = events_result.get('items', [])
    except HttpError as e:
        print(e)

    return render(request, 'events/index.html', context={'events': events})
