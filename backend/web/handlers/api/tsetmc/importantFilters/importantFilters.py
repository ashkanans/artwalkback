from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.tsetmc.service import TsetmcService


class TsetmcImportantfiltersHandler:
    def __init__(self, authenticator: Authenticator):
        self.tsetmc_service = TsetmcService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            sort_by = request.args.get('sort_by', '')
            sort_order = request.args.get('sort_order', 'asc')

            important_filters = self.tsetmc_service.get_important_filters(sort_by=sort_by, sort_order=sort_order)

            data = [importantFilter.to_dict() for importantFilter in important_filters]
            self.response = {'data': data}
            return self.response
        else:
            return self.authenticator.message
