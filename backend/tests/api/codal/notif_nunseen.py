from backend.tests.api.BaseTestCase import BaseAPITestCase


class TestCodalNotifNUnseen(BaseAPITestCase):

    def test_get_NUnseen(self):
        response = self.client.post('/api/codal/notification/NUnseen',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertIsNotNone(response_data)

    def test_unauthorized_access_no_token(self):
        self.unauthorized_access_no_token('/api/tsetmc/returnInfo')

    def test_unauthorized_access_wrong_token(self):
        self.unauthorized_access_wrong_token('/api/tsetmc/returnInfo')
