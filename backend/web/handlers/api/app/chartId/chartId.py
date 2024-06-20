from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.model.app.chart_id import ids_list_to_dict_list
from backend.web.service.app.service import AppService


class AppChartidHandler:
    def __init__(self, authenticator: Authenticator):
        self.appService = AppService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            sort_by = request.args.get('sort_by', '')
            sort_order = request.args.get('sort_order', 'asc')

            ids_list = self.appService.get_chart_ids(sort_by=sort_by, sort_order=sort_order)

            ids_dict = ids_list_to_dict_list(ids_list)

            self.response = ids_dict
            return self.response
        else:
            return self.authenticator.message
