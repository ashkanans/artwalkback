from backend.tests.api.AWBaseTestCase import ArtWalkBaseAPITestCase
from web_app import app


class AWTestPredict(ArtWalkBaseAPITestCase):

    def test_api_predict(self):
        self.start_id = "ChIJ1UCDJ1NgLxMRtrsCzOHxdvY"
        self.end_id = "ChIJKcGbg2NgLxMRthZkUqDs4M8"
        self.time_span = 120 * 60
        response = self.client.post('/api/artwalk/predict', json={
            'start_id': self.start_id,
            'end_id': self.end_id,
            'time_span': self.time_span
        })

        # Check if the server works properly
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json)

        # Validate the response content
        json_data = response.get_json()
        self.assertIn('recommended_path', json_data)
        self.assertIn('display_names', json_data)

        # Check if the recommended path and display names are not empty
        self.assertGreater(len(json_data['recommended_path']), 0)
        self.assertGreater(len(json_data['display_names']), 0)
