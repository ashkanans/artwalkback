from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES
from backend.web.service.setting.service import SettingService


class SettingSetHandler:
    def __init__(self, authenticator: Authenticator):
        self.settingService = SettingService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            setting_values = request.get_json()
            user_agent = request.headers.get('User-Agent')
            if 'Mobi' in user_agent:
                device_type = 'mobile'
            else:
                device_type = 'pc'
            self.settingService.set_setting_by_user(self.authenticator.user_id, setting_values, device_type)

            return MESSAGES['SETTING']['SUCCESSFUL_SET']
        else:
            return self.authenticator.message
