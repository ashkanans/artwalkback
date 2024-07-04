from backend.tests.api.AWBaseTestCase import ArtWalkBaseAPITestCase
from web_app import app


class AWTestPlaceTypes(ArtWalkBaseAPITestCase):

    def test_api_placeTypes(self):
        client = app.test_client()

        response = client.post('/api/artwalk/predict',
                               json={'username': self.username, 'password': self.password})

        # Check if the server works properly
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.json)
