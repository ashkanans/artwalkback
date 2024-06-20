from backend.tests.api.BaseTestCase import BaseAPITestCase


class TestCodalNotifConfigs(BaseAPITestCase):

    def test_set_notif_config(self):
        steps = {
            "step1": {
                "including": "دادگاه، شرکت",
                "excluding": "دلار، يورو"
            },
            "step2": [
                "10260085303",
                "10101138294"
            ],
            "step3": [
                "1"
            ],
            "step4": {
                "period": "1",
                "lettersChecked": True,
                "attachmentsChecked": True
            }
        }

        response = self.client.post('/api/codal/notification/configuration/set',
                                    json=steps,
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertIsNotNone(response_data)

    def test_user_get_notif_config(self):
        response = self.client.post('/api/codal/notification/configuration/get',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertIsNotNone(response_data)

    def test_unauthorized_access_no_token(self):
        self.unauthorized_access_no_token('/api/tsetmc/returnInfo')

    def test_unauthorized_access_wrong_token(self):
        self.unauthorized_access_wrong_token('/api/tsetmc/returnInfo')
