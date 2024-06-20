from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.model.setting import Setting
from backend.web.service.setting.service import SettingService


class SettingGetHandler:
    def __init__(self, authenticator: Authenticator):
        self.settingService = SettingService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            user_agent = request.headers.get('User-Agent')
            if 'Mobi' in user_agent:
                device_type = 'mobile'
            else:
                device_type = 'pc'

            settings = self.settingService.get_setting_by_user_id_device_type(self.authenticator.user_id, device_type)

            self.response = Setting().to_dict_list(settings)

            return self.response
        else:
            return self.authenticator.message
