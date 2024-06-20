from unittest import TestCase

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES
from backend.web.service.user import UserService
from web_app import app


class TestCommodityBiList(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.user_service = UserService()
        self.username = 'example'
        self.password = 'example'
        self.email = 'example.com'

        self.user = self.user_service.create_user(username=self.username, password=self.password, email=self.email)

        self.token = Authenticator().generate_auth_token(user_id=self.user.user_id, username=self.username)

    def tearDown(self):
        self.user_service.delete_user_by_username(self.username)

    def test_get_commodity_bi_list(self):
        id = 137131
        from_date = "2024/02/09"
        to_date = "2024/04/09"
        date_type = "gr"
        response = self.client.post(
            f'/api/commodity/bi/list?id={id}&from_date={from_date}&to_date={to_date}&date_type={date_type}',
                                    json={},
                                    headers={'Authorization': 'Bearer ' + self.token})

        self.assertEqual(response.status_code, 200)

        # The expected keys for each dictionary
        expected_keys = [
            'ID', 'category', 'category_fa', 'Name_fa', 'Name_en', 'Unit'
        ]

        response_data = response.json

        # Check if the response contains data
        self.assertTrue(response_data)

        # Check if the response contains data
        self.assertTrue(response_data['data'])

        self.assertTrue(response_data['data']['category'])
        self.assertTrue(response_data['data']['category_id'])
        self.assertTrue(response_data['data']['list'])
        self.assertTrue(response_data['data']['name_fa'])

    def test_unauthorized_access_no_token(self):
        # Simulate a request to the endpoint without authentication token
        id = 85
        from_date = "2023-02-09"
        to_date = "2024-02-09"
        response = self.client.post(f'/api/commodity/bi/list?id={id}&from_date={from_date}&to_date={to_date}',
                                    json={}
                                    )

        # Check if the server returns unauthorized access message
        self.assertEqual(response.json, MESSAGES['AUTHENTICATION']['TOKEN_NOT_FOUND'])

    def test_unauthorized_access_wrong_token(self):
        # Simulate a request to the endpoint with a wrong authentication token

        # A dummy token
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCIsImlzcyI6InVybjpmb28ifQ.q238-_0A-EYXy0Xt12zJURTbzu_5liY94GnlpBVy7eA'
        id = 85
        from_date = "2023-02-09"
        to_date = "2024-02-09"
        response = self.client.post(f'/api/commodity/bi/list?id={id}&from_date={from_date}&to_date={to_date}',
                                    json={},
                                    headers={'Authorization': 'Bearer ' + token})

        # Check if the server returns {'message': 'Not authorized'}
        self.assertEqual(response.json, MESSAGES['AUTHENTICATION']['NOT_AUTHORIZED'])
