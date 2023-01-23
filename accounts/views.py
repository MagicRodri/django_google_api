import google_auth_oauthlib.flow
from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from events.models import Calendar, Event
from events.tasks import get_events_from_api
from events.utils import get_calendar_list, get_events

from .models import GoogleCredential
from .utils import credentials_to_dict

CALENDAR_API_SCOPES = settings.CALENDAR_API_SCOPES
User = get_user_model()


class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['google_oauth_client_id'] = settings.GOOGLE_OAUTH_CLIENT_ID
        context['google_oauth_redirect_uri'] = reverse('accounts:google_login')
        return context


class LogoutView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            self.request.session.flush()
            logout(self.request)
        return redirect('home')


@csrf_exempt
def google_login(request):
    csrf_token_cookie = request.COOKIES.get('g_csrf_token')
    if not csrf_token_cookie:
        return HttpResponse('Missing CSRF token cookie', status=403)
    csrf_token_body = request.POST.get('g_csrf_token')
    if not csrf_token_body:
        return HttpResponse('Missing CSRF token', status=403)
    if csrf_token_cookie != csrf_token_body:
        return HttpResponse('CSRF token mismatch', status=403)

    if request.method == 'POST':
        token = request.POST.get('credential')
        try:
            idinfo = id_token.verify_oauth2_token(
                token, google_requests.Request(),
                settings.GOOGLE_OAUTH_CLIENT_ID)
            if idinfo['iss'] not in [
                    'accounts.google.com', 'https://accounts.google.com'
            ]:
                raise ValueError('Wrong issuer.')

            user, created = User.objects.get_or_create(google_id=idinfo['sub'],
                                                       email=idinfo.get(
                                                           'email', ''))
            if created:
                user.first_name = idinfo.get('given_name', '')
                user.last_name = idinfo.get('family_name', '')
                user.username = idinfo.get('email', '')
                user.save()
            login(request, user)
        except ValueError:
            return HttpResponse('Invalid token', status=400)
        return redirect('home')


@login_required
def google_auth(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=CALENDAR_API_SCOPES,
    )
    redirect_uri = request.build_absolute_uri(
        reverse('accounts:google_auth_callback'))
    flow.redirect_uri = redirect_uri
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')
    request.session['state'] = state
    return redirect(authorization_url)


@login_required
def google_auth_callback(request):
    state = request.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=CALENDAR_API_SCOPES,
        state=state)

    flow.redirect_uri = request.build_absolute_uri(
        reverse('accounts:google_auth_callback'))

    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)
    defaults = {
        'scopes': ','.join(credentials.scopes),
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'client_id': credentials.client_id
    }
    GoogleCredential.objects.update_or_create(user=request.user,
                                              defaults=defaults)
    calendars = get_calendar_list(credentials)
    Calendar.from_calendar_list(request.user, calendars)
    for calendar in calendars:
        if calendar:
            events = get_events(credentials, calendar['id'])
            calendar = Calendar.objects.get(user=request.user,
                                            calendar_id=calendar['id'])
            Event.from_events_list(request.user, calendar, events)
    # get_events_from_api.apply_async(args=(request.user.id,
    #                                       request.session['credentials']))
    return redirect('events:list')