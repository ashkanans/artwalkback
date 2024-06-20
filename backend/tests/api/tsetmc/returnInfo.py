from backend.tests.api.BaseTestCase import BaseAPITestCase


class TestTsetmcReturnInfo(BaseAPITestCase):

    def test_get_index_info(self):
        response = self.client.post('/api/tsetmc/returnInfo',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertIsNotNone(response_data)

        # Assert the structure of the response
        self.assertTrue('stock' in response_data)
        self.assertTrue('industrial' in response_data)
        self.assertTrue('market' in response_data)


    def test_get_sorted_return_info(self):
        response = self.client.post('/api/tsetmc/returnInfo?sort_by=symbol&sort_order=asc',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        response_data = response.json.get('industrial', [])

        response_first_element = response_data["10 روز"][0]
        response_last_element = response_data["10 روز"][-1]
        self.assertTrue(response_first_element["symbol"] <= response_last_element["symbol"])

    def test_unauthorized_access_no_token(self):
        self.unauthorized_access_no_token('/api/tsetmc/returnInfo')

    def test_unauthorized_access_wrong_token(self):
        self.unauthorized_access_wrong_token('/api/tsetmc/returnInfo')
