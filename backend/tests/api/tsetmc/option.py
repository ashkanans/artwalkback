from backend.tests.api.BaseTestCase import BaseAPITestCase


class TestTsetmcReturnInfo(BaseAPITestCase):

    def test_get_options(self):
        response = self.client.post('/api/tsetmc/option',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertIsNotNone(response_data)

        # Assert the structure of the response
        self.assertTrue('base' in response_data[0])
        self.assertTrue('call' in response_data[0])
        self.assertTrue('put' in response_data[0])

    def test_unauthorized_access_no_token(self):
        self.unauthorized_access_no_token('/api/tsetmc/returnInfo')

    def test_unauthorized_access_wrong_token(self):
        self.unauthorized_access_wrong_token('/api/tsetmc/returnInfo')
