
from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.index_info import IndexInfoService


class TsetmcIndexInfoHandler:
    def __init__(self, authenticator: Authenticator):
        self.index_info_service = IndexInfoService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            sort_by = request.args.get('sort_by', '')
            sort_order = request.args.get('sort_order', 'asc')

            all_index_info = self.index_info_service.get_all_index_info(sort_order=sort_order, sort_by=sort_by)
            self.response = {'market': [index_info.to_dict() for index_info in all_index_info]}
            return self.response
        else:
            return self.authenticator.message
