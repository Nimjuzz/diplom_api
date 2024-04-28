from django.conf import settings
import requests


class GoogleOAuthService:

    @classmethod
    def exchange_code_for_token(cls, auth_code):
        data = {
            'code': auth_code,
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_OAUTH2_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        response = requests.post('https://oauth2.googleapis.com/token', data=data)
        response.raise_for_status()
        return response.json().get('access_token')

    @classmethod
    def fetch_user_profile(cls, access_token):
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get('https://www.googleapis.com/oauth2/v3/userinfo', headers=headers)
        response.raise_for_status()
        return response.json()

