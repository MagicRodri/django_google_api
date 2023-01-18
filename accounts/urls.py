from django.urls import path

from .views import google_auth, google_auth_callback

urlpatterns = [
    path('google-auth/', google_auth, name='google_auth'),
    path('google-auth-callback/',
         google_auth_callback,
         name='google_auth_callback'),
]
