from unittest import TestCase

from backend.web.handlers.api.messages import MESSAGES
from backend.web.service.user import UserService
from web_app import app


class TestSignup(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user_service = UserService()
        self.username = 'example1'
        self.password = 'example1'
        self.email = 'example.com1'
        self.name = 'example'
        self.sirname = 'example'

    def tearDown(self):
        self.user_service.delete_user_by_username(self.username)

    def test_api_user_signup(self):
        client = app.test_client()

        response = client.post('/api/signup',
                               json={'username': self.username, 'password': self.password,
                                     'email': self.email, 'name': self.name, 'sirname': self.sirname})

        # Check if the server works properly
        self.assertEqual(response.status_code, 200)

        # Checking if the response contains the expected JSON data
        self.assertEqual(response.json, MESSAGES['AUTHENTICATION']['REGISTRATION_SUCCESSFUL'])

    def test_api_user_signup_failed(self):
        client = app.test_client()

        response = client.post('/api/signup',
                               json={})

        # Check if the server works properly
        self.assertEqual(response.status_code, 200)

        response_data = response.json
        success = response_data.get('success')
        message = response_data.get('message')

        # Checking if the response contains the expected JSON data
        self.assertEqual(success, False)
        self.assertIn("Error registering user", message)
