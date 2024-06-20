from flask import Request
from backend.utils.web.api.tsetmc.utils import stock_info_to_list_dict
from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.tsetmc.service import TsetmcService


class TsetmcStockinfoHandler:
    def __init__(self, authenticator: Authenticator):
        self.tsetmc_service = TsetmcService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            sort_by = request.args.get('sort_by', '')
            sort_order = request.args.get('sort_order', 'asc')

            stocks_info = self.tsetmc_service.get_stocks_info(sort_order=sort_order, sort_by=sort_by)

            data = [stock_info.to_dict() for stock_info in stocks_info]

            self.response = {'data': data}
            return self.response
        else:
            return self.authenticator.message
