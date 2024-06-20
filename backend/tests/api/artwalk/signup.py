from unittest import TestCase

from backend.web.dao.artwalk.users_dao import UsersDAO
from backend.web.handlers.api.messages import MESSAGES
from web_app import app


class AWTestSignup(TestCase):
    def setUp(self):
        self.user_dao = UsersDAO()
        self.username = 'example21'
        self.password = 'example1'
        self.number = '351123123'

    def tearDown(self):
        self.user_dao.delete_user_by_username(self.username)
    def test_api_user_signup(self):
        client = app.test_client()

        response = client.post('/api/artwalk/signup',
                               json={'username': self.username, 'password': self.password,
                                     'mobile_number': self.number})

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
