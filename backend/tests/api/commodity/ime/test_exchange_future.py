from unittest import TestCase

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES
from backend.web.service.user import UserService
from web_app import app


class TestImeFuture(TestCase):
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

    def test_get_ime_future(self):
        response = self.client.post('/api/commodity/ime/future',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        # The expected keys for each dictionary
        expected_keys = [
            "ActiveBrokers",
            "ActiveCustomers",
            "C_Buy",
            "C_Sell",
            "ChangeOpenInterest",
            "ContractCode",
            "ContractDay",
            "ContractDescription",
            "DT",
            "DeliveryDate",
            "FirstPrice",
            "LastPrice",
            "LastSettlementPrice",
            "MaxPrice",
            "MinPrice",
            "MonthlyOpenInterests",
            "MonthlyOpenInterestsPercent",
            "MonthlySettlementPrice",
            "MonthlySettlementPricePercent",
            "OpenInterest",
            "SettlementPricePercent",
            "TodaySettlementPrice",
            "TradesValue",
            "TradesVolume",
            "UniqueID",
            "Val_Haghighi_Buy",
            "Val_Haghighi_Sell",
            "Val_Hoghooghi_Buy",
            "Val_Hoghooghi_Sell",
            "Vol_Haghighi_Buy",
            "Vol_Haghighi_Sell",
            "Vol_Hoghooghi_Buy",
            "Vol_Hoghooghi_Sell",
            "WeeklyOpenInterests",
            "WeeklyOpenInterestsPercent",
            "WeeklySettlementPrice",
            "WeeklySettlementPricePercent",

        ]

        response_data = response.json.get('data', [])

        # Check if the response contains data
        self.assertTrue(response_data)

        # Check the structure of the first dictionary in the data list
        first_data = response_data[0]
        for key in expected_keys:
            self.assertIn(key, first_data)

        # Check the structure of the last dictionary in the data list
        last_data = response_data[-1]
        for key in expected_keys:
            self.assertIn(key, last_data)


    def test_get_sorted_ime_future(self):
        response = self.client.post('/api/commodity/ime/future?sort_by=ContractCode&sort_order=asc',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        response_data = response.json.get('data', [])

        # Check if the response contains data
        self.assertTrue(response_data)
        response_first_element = response_data[0]
        response_last_element = response_data[-1]
        self.assertTrue(response_first_element["ContractCode"] <= response_last_element["ContractCode"])

    def test_unauthorized_access_no_token(self):
        # Simulate a request to the endpoint without authentication token
        response = self.client.post('/api/commodity/ime/future',
                                    json={}
                                    )

        # Check if the server returns unauthorized access message
        self.assertEqual(response.json, MESSAGES['AUTHENTICATION']['TOKEN_NOT_FOUND'])

    def test_unauthorized_access_wrong_token(self):
        # Simulate a request to the endpoint with a wrong authentication token

        # A dummy token
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCIsImlzcyI6InVybjpmb28ifQ.q238-_0A-EYXy0Xt12zJURTbzu_5liY94GnlpBVy7eA'
        response = self.client.post('/api/commodity/ime/future',
                                    json={},
                                    headers={'Authorization': "Bearer " + token})

        # Check if the server returns {'message': 'Not authorized'}
        self.assertEqual(response.json, MESSAGES['AUTHENTICATION']['NOT_AUTHORIZED'])
