from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.codal.service import CodalService


class CodalGroupsHandler:
    def __init__(self, authenticator: Authenticator):
        self.codalService = CodalService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:

            groups = self.codalService.get_all_groups()

            unique_report_types = []
            filtered_groups = []
            for group in groups:
                report_type = group.reportTypes
                if report_type not in unique_report_types:
                    filtered_groups.append({'type': group.reportTypes, 'name': group.name})
                    unique_report_types.append(report_type)

            self.response = {'data': filtered_groups}
            return self.response
        else:
            return self.authenticator.message
