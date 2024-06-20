from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.codal.service import CodalService


class CodalSymbolsHandler:
    def __init__(self, authenticator: Authenticator):
        self.codalService = CodalService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:

            publishers = self.codalService.get_all_symbols()

            sorted_publishers = sorted(publishers, key=lambda x: x.Symbol)

            symbols_dict = [{'National_Code': publisher.National_Code, 'Symbol': publisher.Symbol} for publisher in
                            sorted_publishers]

            self.response = {'data': symbols_dict}
            return self.response
        else:
            return self.authenticator.message
