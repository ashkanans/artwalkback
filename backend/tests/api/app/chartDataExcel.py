from backend.tests.api.BaseTestCase import BaseAPITestCase


class TestAppChartData(BaseAPITestCase):

    def test_get_app_chart_data(self):
        # Prepare the request
        headers = {'Authorization': 'Bearer ' + self.token}
        payload = {
            "parameters": ["IRO1KYAN0001", "IRO1GMSH0001", "IRO1BMEL0001", "IRO1PGDR0001_2"],
            "date_range": {
                "from": "2020-07-29",
                "to": "2023-09-29"
            },
            "setting": {
                "file_type": "excel"
            }
        }

        # Send POST request
        response = self.client.post('/api/app/chartDataExcel', json=payload, headers=headers)

        response_json = response.json
        # Assertions
        self.assertEqual(response.status_code, 200)

