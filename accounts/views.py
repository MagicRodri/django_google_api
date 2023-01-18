import google_auth_oauthlib.flow
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

from .utils import credentials_to_dict

SCOPES = ['https://www.googleapis.com/auth/calendar']


def google_auth(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=SCOPES,
    )

    redirect_uri = request.build_absolute_uri(reverse('google_auth_callback'))
    flow.redirect_uri = redirect_uri
    print(redirect_uri)

    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')

    request.session['state'] = state

    return redirect(authorization_url)


def google_auth_callback(request):
    state = request.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS_FILE, scopes=SCOPES, state=state)

    flow.redirect_uri = request.build_absolute_uri(
        reverse('google_auth_callback'))

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    return redirect('events')