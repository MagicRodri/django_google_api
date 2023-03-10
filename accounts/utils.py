from django.shortcuts import redirect

from accounts.models import GoogleCredential


def credentials_to_dict(credentials):
    """
    Convert google.oauth2.credentials.Credentials to dict
    """
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes,
    }


# def validate_google_credentials(request):
#     """
#     Validate google credentials
#     """
#     qs = GoogleCredential.objects.filter(user=self.request.user)
#     if qs.exists():
#         creds = qs.first().to_credentials()
#         if not creds.valid:
#             creds.refresh(Request())


class GoogleCalendarAuthorizationRequiredMixin:
    """
    Mixin for views that checks that the user has authorized the app to
    access their Google Calendar, redirecting to the authorization page if
    necessary.
    """

    def dispatch(self, *args, **kwargs):
        if not 'credentials' in self.request.session:
            return redirect('accounts:google_auth')
        return super().dispatch(self.request, *args, **kwargs)


def calendar_authorization_required(view_func):
    """
    Decorator for views that checks that the user has authorized the app to
    access their Google Calendar, redirecting to the authorization page if
    necessary.
    """

    def _wrapped_view(request, *args, **kwargs):
        if not 'credentials' in request.session:
            return redirect('accounts:google_auth')
        return view_func(request, *args, **kwargs)

    return _wrapped_view