from unittest import TestCase

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES
from backend.web.service.user import UserService
from web_app import app


class TestAppChartData(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user_service = UserService()
        self.username = 'example'
        self.password = 'example'
        self.email = 'example.com'
        self.name = 'example'
        self.sirname = 'example.com'

        self.user = self.user_service.create_user(username=self.username, password=self.password, email=self.email,
                                                  name=self.name, sirname=self.sirname)

        self.token = Authenticator().generate_auth_token(user_id=self.user.user_id, username=self.username)

    def tearDown(self):
        self.user_service.delete_user_by_username(self.username)

    def test_get_app_chart_data(self):
        id = "IRO3GPHP0001"
        from_date = "2017-07-29"
        to_date = "2017-09-29"
        date_type = "gr"
        response = self.client.post(
            f'/api/app/chartData?id={id}&from_date={from_date}&to_date={to_date}&date_type={date_type}',
            json={},
            headers={'Authorization': 'Bearer ' + self.token})

        self.assertEqual(response.status_code, 200)

        response_data = response.json

        # Check if the response contains data
        self.assertTrue(response_data)

        # Check if the response contains data
        self.assertTrue(response_data['data'])

        self.assertTrue(response_data['data']['level1'])
        self.assertTrue(response_data['data']['level2'])
        self.assertTrue(response_data['data']['level3'])
        self.assertTrue(response_data['data']['level4'])
        self.assertTrue(response_data['data']['level4_id'])
        self.assertTrue(response_data['data']['list'])

    def test_unauthorized_access_no_token(self):
        # Simulate a request to the endpoint without authentication token
        response = self.client.post(f'/api/app/chartData',
                                    json={}
                                    )

        # Check if the server returns unauthorized access message
        self.assertEqual(response.json, MESSAGES['AUTHENTICATION']['TOKEN_NOT_FOUND'])

    def test_unauthorized_access_wrong_token(self):
        # Simulate a request to the endpoint with a wrong authentication token

        # A dummy token
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCIsImlzcyI6InVybjpmb28ifQ.q238-_0A-EYXy0Xt12zJURTbzu_5liY94GnlpBVy7eA'
        response = self.client.post(f'/api/app/chartData',
                                    json={},
                                    headers={'Authorization': 'Bearer ' + token})

        # Check if the server returns {'message': 'Not authorized'}
        self.assertEqual(response.json, MESSAGES['AUTHENTICATION']['NOT_AUTHORIZED'])
