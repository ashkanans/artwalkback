from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.model.app.chart_data import data_list_to_dict
from backend.web.service.app.service import AppService


class AppChartdataHandler:
    def __init__(self, authenticator: Authenticator):
        self.appService = AppService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            sort = request.args.get('sort')
            id = request.args.get('id')
            date_type = request.args.get('date_type')
            from_date = request.args.get('from_date')
            to_date = request.args.get('to_date')

            if not id or not from_date or not to_date:
                return {
                    'error': f'Not supported parameter, Please upload check the given paramters: id= {id}, from_date= {from_date}, to_date= {to_date}'}

            data_list = self.appService.get_chart_data(id=id, from_date=from_date, to_date=to_date,
                                                       date_type=date_type)
            data_dict = data_list_to_dict(data_list)
            data_list_id = self.appService.get_chartId_by_id(id=id)

            self.response = {"data": {
                "level1": data_list_id.level1,
                "level2": data_list_id.level2,
                "level3": data_list_id.level3,
                "level4": data_list_id.level4,
                "level4_id": data_list_id.level4_id,
                "list": data_dict}
            }

            return self.response
        else:
            return self.authenticator.message
