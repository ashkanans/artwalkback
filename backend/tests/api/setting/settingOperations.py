from backend.tests.api.BaseTestCase import BaseAPITestCase
from backend.web.handlers.api.messages import MESSAGES
from backend.web.service.setting.service import SettingService


class TestSettingOperations(BaseAPITestCase):

    def tearDown(self):
        self.user_service.delete_user_by_username(self.username)
        SettingService().delete_rows_by_user_id(self.user.user_id)

    def test_set_setting(self):
        data = {
            'table-columns': 'TABLE_COLUMNS_VALUE',
            'day-or-night': "day",
            'layout-grid': 'LAYOUT_GRID_VALUE'
        }

        response = self.client.post('/api/setting/set',
                                    json=data,
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.json, MESSAGES['SETTING']['SUCCESSFUL_SET'])

    def test_user_get_setting(self):
        self.test_set_setting()
        response = self.client.post('/api/setting/get',
                                    json={},
                                    headers={'Authorization': "Bearer " + self.token})

        self.assertEqual(response.status_code, 200)

        response_data = response.json
        self.assertIsNotNone(response_data[0])
        self.assertIsNotNone(response_data[1])
        self.assertIsNotNone(response_data[2])

    def test_set_unauthorized_access_no_token(self):
        self.unauthorized_access_no_token('/api/setting/set')

    def test_set_unauthorized_access_wrong_token(self):
        self.unauthorized_access_wrong_token('/api/setting/set')

    def test_get_unauthorized_access_no_token(self):
        self.unauthorized_access_no_token('/api/setting/get')

    def test_get_unauthorized_access_wrong_token(self):
        self.unauthorized_access_wrong_token('/api/setting/get')
