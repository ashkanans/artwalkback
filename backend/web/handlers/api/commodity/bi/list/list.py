from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.model.business_insider.price_history import bi_data_list_to_dict
from backend.web.service.business_insider.service import BIService


class CommodityBiListHandler:
    def __init__(self, authenticator: Authenticator):
        self.businessInsiderService = BIService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            id = request.args.get('id')
            date_type = request.args.get('date_type')
            from_date = request.args.get('from_date')
            to_date = request.args.get('to_date')

            if not id or not from_date or not to_date:
                return {
                    'error': f'Not supported parameter, Please upload check the given paramters: id= {id}, from_date= {from_date}, to_date= {to_date}'}

            data_list = self.businessInsiderService.get_relative_data(id=id, from_date=from_date, to_date=to_date,
                                                                      date_type=date_type)
            data_dict = bi_data_list_to_dict(data_list)
            data_list_id = self.businessInsiderService.get_bi_ids_by_id(id=id)

            self.response = {"data": {
                "name_fa": data_list_id.Name_fa,
                "category": data_list_id.category_fa,
                                    "category_id": data_list_id.category_id,
                                    "list": data_dict}
                             }

            return self.response
        else:
            return self.authenticator.message
