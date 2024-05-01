from django.urls import path, include

from .views import GoogleLoginRedirectView, GoogleAuthURL

urlpatterns = [
    path('auth/google/url/', GoogleAuthURL.as_view(), name='google_auth_url'),
    path('auth/google/callback/', GoogleLoginRedirectView.as_view(), name='google_callback'),
]