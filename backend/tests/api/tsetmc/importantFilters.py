from backend.tests.api.BaseTestCase import BaseAPITestCase


class TestImportantFiltersInfo(BaseAPITestCase):

    def test_get_important_filters(self):
        response = self.client.post('/api/tsetmc/importantFilters',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        # The expected keys for each dictionary
        expected_keys = [
            "tse_id_2",
            "Persian_symbol",
            "first_price",
            "Final_price",
            "last_price",
            "Number_transactions",
            "Vol",
            "Value",
            "Yesterday_price",
            "per_change_price",
            "status",
            "queue_value",
            "perc_last",
            "volume_ratio_to_month",
            "buy_per_capita",
            "sell_per_capita",
            "entered_money",
            "buyer_power"
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


    def test_get_sorted_important_filters(self):
        response = self.client.post('/api/tsetmc/importantFilters?sort_by=Final_price&sort_order=asc',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        response_data = response.json.get('data', [])


        response_first_element = response_data[0]
        response_last_element = response_data[-1]
        self.assertTrue(response_first_element["Final_price"] <= response_last_element["Final_price"])
    def test_unauthorized_access_no_token(self):
        self.unauthorized_access_no_token('/api/tsetmc/importantFilters')

    def test_unauthorized_access_wrong_token(self):
        self.unauthorized_access_wrong_token('/api/tsetmc/importantFilters')

    def test_get_important_filters_with_sort_args(self):
        response = self.client.post('/api/tsetmc/importantFilters?sort=Final_price:desc',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        # The expected keys for each dictionary
        expected_keys = [
            "tse_id_2",
            "Persian_symbol",
            "first_price",
            "Final_price",
            "last_price",
            "Number_transactions",
            "Vol",
            "Value",
            "Yesterday_price",
            "per_change_price",
            "status",
            "queue_value",
            "perc_last",
            "volume_ratio_to_month",
            "buy_per_capita",
            "sell_per_capita",
            "entered_money",
            "buyer_power"
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

        self.assertGreaterEqual(first_data['Final_price'], last_data['Final_price'])
