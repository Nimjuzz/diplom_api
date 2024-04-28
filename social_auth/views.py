from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import ValidationError

import requests
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError


from accounts.models import CustomUser
from social_auth.services import GoogleOAuthService


class GoogleAuthURL(APIView):
    AUTH_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth?"

    def get_auth_url(self):
        auth_url = (
            f"{self.AUTH_BASE_URL}"
            f"client_id={settings.GOOGLE_OAUTH2_CLIENT_ID}"
            f"&redirect_uri={settings.GOOGLE_OAUTH2_REDIRECT_URI}"
            "&response_type=code"
            "&scope=email&access_type=offline"
        )
        return auth_url

    def get(self, request, *args, **kwargs):
        return Response({"auth_url": self.get_auth_url()})


class GoogleLoginRedirectView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    def get(self, request, *args, **kwargs):
        auth_code = request.GET.get('code')
        if not auth_code:
            return self._error_response('Authorization code not provided.')

        try:
            access_token = GoogleOAuthService.exchange_code_for_token(auth_code)
            profile_info = GoogleOAuthService.fetch_user_profile(access_token)
            user = self._get_or_create_user(profile_info)
            token = self._get_or_create_token(user)

        except (ValidationError, requests.RequestException) as e:
            return self._error_response(str(e))

        return JsonResponse({"token": token.key, "user_id": user.id})

    def _get_or_create_user(self, profile_info):
        user, _ = CustomUser.objects.get_or_create(email=profile_info['email'])
        return user

    def _get_or_create_token(self, user):
        token, created = Token.objects.get_or_create(user=user)
        return token

    def _error_response(self, error_message):
        return JsonResponse({'error': error_message}, status=400)