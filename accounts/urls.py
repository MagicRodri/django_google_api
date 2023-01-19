from django.urls import path

from .views import LoginView, google_auth, google_auth_callback, google_login

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('login/google/', google_login, name='google_login'),
    path('google-auth/', google_auth, name='google_auth'),
    path('google-auth-callback/',
         google_auth_callback,
         name='google_auth_callback'),
]
