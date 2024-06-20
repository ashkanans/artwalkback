from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.codal.service import CodalService


class CodalNotificationConfigurationGetHandler:
    def __init__(self, authenticator: Authenticator):
        self.codalService = CodalService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:

            config = self.codalService.get_notitification_configutaion_by_user_id(self.authenticator.user_id)
            if config is not None:
                self.response = {'data': config}
            else:
                config = {
                    'user_id': '',
                    'including': '',
                    'excluding': '',
                    'publisher_national_code': '',
                    'letter_types': '',
                    'period': '',
                    'lettersChecked': '',
                    'attachmentsChecked': '',
                    'created_datetime': ''
                }
                self.response = {'data': config}
            return self.response
        else:
            return self.authenticator.message
