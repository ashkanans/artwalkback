from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.codal.service import CodalService


class CodalNotificationNunseenHandler:
    def __init__(self, authenticator: Authenticator):
        self.codalService = CodalService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:

            self.response = {"data": self.codalService.get_notification_n_not_seen(self.authenticator.user_id)}

            return self.response
        else:
            return self.authenticator.message
