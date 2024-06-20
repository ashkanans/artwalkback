from backend.tests.api.AWBaseTestCase import ArtWalkBaseAPITestCase
from backend.web.handlers.api.authenticator import Authenticator
from web_app import app


class AWTestPlaces(ArtWalkBaseAPITestCase):

    def test_api_places(self):
        client = app.test_client()

        response = client.post('/api/artwalk/places',
                               json={'username': self.username, 'password': self.password})

        # Check if the server works properly
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.json)


