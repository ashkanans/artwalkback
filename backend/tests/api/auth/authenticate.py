from backend.tests.api.BaseTestCase import BaseAPITestCase
from backend.web.handlers.api.authenticator import Authenticator
from web_app import app


class TestAuthenticate(BaseAPITestCase):

    def test_api_token_based_authentication(self):
        client = app.test_client()

        response = client.post('/api/authenticate',
                               json={'username': self.username, 'password': self.password})

        # Check if the server works properly
        self.assertEqual(response.status_code, 200)

        token = Authenticator().generate_auth_token(user_id=self.user.user_id, username=self.user.username)

        # Checking if the response contains the expected JSON data
        expected_keys = [
            'token', 'message', 'user'
        ]

        response_data = response.json

        for key in expected_keys:
            self.assertIn(key, response_data)

        # Checking the token verification
        response_data_expected = (True, self.user.username, self.user.user_id)
        self.assertEqual(response_data_expected, Authenticator().verify_auth_token(token))
