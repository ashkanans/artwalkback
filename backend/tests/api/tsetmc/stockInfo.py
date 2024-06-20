from backend.tests.api.BaseTestCase import BaseAPITestCase


class TestTsetmcStockInfo(BaseAPITestCase):

    def test_get_stocks_info(self):
        response = self.client.post('/api/tsetmc/stockInfo',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        # The expected keys for each dictionary
        expected_keys = [
            'tse_id', 'Company Name', 'Persian symbol', 'Industry Group', 'perc_final',
            'perc_last', 'Value', 'Vol', 'market_cap', 'Final_price', 'first_price',
            'last_price', 'Yesterday_price', 'Number_transactions', 'volume_ratio_to_month',
            'buy_per_capita', 'sell_per_capita', 'entered_money', 'buyer_power', 'status', 'queue value'
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


    def test_get_sorted_stock_info(self):
        response = self.client.post('/api/tsetmc/stockInfo?sort_by=Value&sort_order=asc',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        response_data = response.json.get('data', [])

        response_first_element = response_data[0]
        response_last_element = response_data[-1]
        self.assertTrue(response_first_element["Value"] <= response_last_element["Value"])

    def test_unauthorized_access_no_token(self):
        self.unauthorized_access_no_token('/api/tsetmc/stockInfo')

    def test_unauthorized_access_wrong_token(self):
        self.unauthorized_access_wrong_token('/api/tsetmc/stockInfo')

    def test_get_stocks_info_with_sort_args(self):
        response = self.client.post('/api/tsetmc/stockInfo?sort=perc_final:desc,Vol:asc',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        # The expected keys for each dictionary
        expected_keys = [
            'tse_id', 'Company Name', 'Persian symbol', 'Industry Group', 'perc_final',
            'perc_last', 'Value', 'Vol', 'market_cap', 'Final_price', 'first_price',
            'last_price', 'Yesterday_price', 'Number_transactions', 'volume_ratio_to_month',
            'buy_per_capita', 'sell_per_capita', 'entered_money', 'buyer_power', 'status', 'queue value'
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
