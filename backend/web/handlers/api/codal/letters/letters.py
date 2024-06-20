from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.codal.service import CodalService


class CodalNotificationOptionsHandler:
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

            periods = [
                {'value': 1, 'name': '۲۴ ساعت گذشته'},
                {'value': 7, 'name': 'یک هفته گذشته'},
                {'value': 14, 'name': 'دو هفته گذشته'},
                {'value': 30, 'name': 'سی روز گذشته'}
            ]

            publishers = self.codalService.get_all_symbols()

            sorted_publishers = sorted(publishers, key=lambda x: x.Symbol)

            symbols_dict = [{'National_Code': publisher.National_Code, 'Symbol': publisher.Symbol} for publisher in
                            sorted_publishers]

            self.response = {'groups': filtered_groups,
                             'periods': periods,
                             'symbols': symbols_dict}

            return self.response
        else:
            return self.authenticator.message
