from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.model.business_insider.id import ids_list_to_dict_list
from backend.web.service.business_insider.service import BIService


class CommodityBiIdsHandler:
    def __init__(self, authenticator: Authenticator):
        self.businessInsiderService = BIService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            ids_list = self.businessInsiderService.get_bi_ids()

            ids_dict = ids_list_to_dict_list(ids_list)

            self.response = ids_dict
            return self.response
        else:
            return self.authenticator.message
