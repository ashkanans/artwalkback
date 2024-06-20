from backend.tests.api.BaseTestCase import BaseAPITestCase


class TestTsetmcEnteredMoney(BaseAPITestCase):
    def test_get_index_info(self):
        response = self.client.post('/api/tsetmc/enteredMoney',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertIsNotNone(response_data)

        # Assert the structure of the response
        self.assertTrue('stock' in response_data)
        self.assertTrue('industry' in response_data)
        self.assertTrue('high_enter_money' in response_data['stock'])
        self.assertTrue('high_exit_money' in response_data['stock'])
        self.assertTrue('high_enter_money' in response_data['industry'])
        self.assertTrue('high_exit_money' in response_data['industry'])

    def test_get_sorted_entered_money(self):
        response = self.client.post('/api/tsetmc/enteredMoney?sort_by=Persian_symbol&sort_order=asc',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        response_data = response.json.get('industry', [])

        # Check if the response contains data
        self.assertTrue(response_data)

        response_first_element = response_data["high_enter_money"]["10 روز"][0]
        response_last_element = response_data["high_enter_money"]["10 روز"][-1]
        self.assertTrue(response_first_element["Persian_symbol"] <= response_last_element["Persian_symbol"])

    def test_unauthorized_access_no_token(self):
        self.unauthorized_access_no_token('/api/tsetmc/enteredMoney')

    def test_unauthorized_access_wrong_token(self):
        self.unauthorized_access_wrong_token('/api/tsetmc/enteredMoney')
