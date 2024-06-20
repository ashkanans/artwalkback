from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.model.tsetmc.option import option_to_dict
from backend.web.service.tsetmc.service import TsetmcService


class TsetmcOptionHandler:
    def __init__(self, authenticator: Authenticator):
        self.tsetmc_service = TsetmcService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:

            options_dict = self.tsetmc_service.get_options()
            self.response = [option_to_dict(option) for option in options_dict.values()]
            return self.response
        else:
            return self.authenticator.message
