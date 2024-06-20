from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.codal.service import CodalService


class CodalNotificationListHandler:
    def __init__(self, authenticator: Authenticator):
        self.codalService = CodalService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:

            self.response = self.codalService.get_letters_notifs_by_user_id(self.authenticator.user_id)

            return self.response
        else:
            return self.authenticator.message
