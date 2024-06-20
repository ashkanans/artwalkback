from flask import Request
from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.new_ime import NewImeService


class CommodityImePremiumHandler:
    def __init__(self, authenticator: Authenticator):
        self.imeService = NewImeService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            sort_by = request.args.get('sort_by', '')
            sort_order = request.args.get('sort_order', 'asc')
            premium_list = self.imeService.get_premium_list(sort_by=sort_by, sort_order=sort_order);

            data = [premium.to_dict() for premium in premium_list]

            self.response = {'data': data}
            return self.response
        else:
            return self.authenticator.message
