from unittest import TestCase
from unittest.mock import patch
from .services import GoogleOAuthService


class GoogleOAuthServiceTests(TestCase):

    def setUp(self):
        # Этот код будет запущен перед каждым тестом
        self.auth_code = 'sample_auth_code'
        self.access_token = 'sample_access_token'
        self.user_info = {
            'email': 'test@example.com',
            'name': 'Test User',
            'sub': '12345'
        }

    @patch('requests.post')
    def test_exchange_code_for_token(self, mock_post):
        # Здесь мы "мокаем" ответ от requests.post
        mock_post.return_value.json.return_value = {'access_token': self.access_token}
        mock_post.return_value.raise_for_status.return_value = None  # Не вызывать исключение

        token = GoogleOAuthService.exchange_code_for_token(self.auth_code)

        self.assertEqual(token, self.access_token)
        mock_post.assert_called_once()

    @patch('requests.get')
    def test_fetch_user_profile(self, mock_get):
        # Здесь мы "мокаем" ответ от requests.get
        mock_get.return_value.json.return_value = self.user_info
        mock_get.return_value.raise_for_status.return_value = None  # Не вызывать исключение

        profile = GoogleOAuthService.fetch_user_profile(self.access_token)

        self.assertEqual(profile, self.user_info)
        mock_get.assert_called_once_with(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )