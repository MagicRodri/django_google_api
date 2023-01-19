from django.shortcuts import redirect


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


class GoogleCalendarAuthorizationRequiredMixin:
    """
    Mixin for views that checks that the user has authorized the app to
    access their Google Calendar, redirecting to the authorization page if
    necessary.
    """

    def dispatch(self, request, *args, **kwargs):
        if 'credentials' not in request.session:
            return redirect('accounts:google_auth')
        return super().dispatch(request, *args, **kwargs)


def calendar_authorization_required(view_func):
    """
    Decorator for views that checks that the user has authorized the app to
    access their Google Calendar, redirecting to the authorization page if
    necessary.
    """

    def _wrapped_view(request, *args, **kwargs):
        if 'credentials' not in request.session:
            return redirect('accounts:google_auth')
        return view_func(request, *args, **kwargs)

    return _wrapped_view