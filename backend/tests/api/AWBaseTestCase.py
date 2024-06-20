from unittest import TestCase

from backend.web.dao.artwalk.users_dao import UsersDAO
from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES
from web_app import app


class ArtWalkBaseAPITestCase(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user_dao = UsersDAO()
        self.username = 'example'
        self.password = 'example'
        self.email = 'example.com'
        self.mobileNumber = '351555555'

        self.user = self.user_dao.insert_user(username=self.username, password=self.password,
                                              mobile_phone=self.mobileNumber)
        self.token = Authenticator().generate_auth_token(user_id=self.user.user_id, username=self.username)

    def tearDown(self):
        self.user_dao.delete_user_by_username(self.username)

    def unauthorized_access_no_token(self, url):
        # Simulate a request to the endpoint without authentication token
        response = self.client.post(url, json={})

        # Check if the server returns unauthorized access message
        self.assertEqual(response.json, MESSAGES['AUTHENTICATION']['TOKEN_NOT_FOUND'])

    def unauthorized_access_wrong_token(self, url):
        # Simulate a request to the endpoint with a wrong authentication token

        # A dummy token
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCIsImlzcyI6InVybjpmb28ifQ.q238-_0A-EYXy0Xt12zJURTbzu_5liY94GnlpBVy7eA'
        response = self.client.post(url, json={}, headers={'Authorization': "Bearer " + token})

        # Check if the server returns {'message': 'Not authorized'}
        self.assertEqual(response.json, MESSAGES['AUTHENTICATION']['NOT_AUTHORIZED'])
