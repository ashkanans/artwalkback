from flask import Request
from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.new_ime import NewImeService


class CommodityImeMainGroupsHandler:
    def __init__(self, authenticator: Authenticator):
        self.imeService = NewImeService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            main_groups = self.imeService.get_main_groups()

            data = [{"name": item.Name, "code": item.code} for item in main_groups]

            self.response = {'data': data}
            return self.response
        else:
            return self.authenticator.message
