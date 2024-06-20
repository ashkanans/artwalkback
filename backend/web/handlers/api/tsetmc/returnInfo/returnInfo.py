from collections import defaultdict

from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.tsetmc.service import TsetmcService


class TsetmcReturninfoHandler:
    def __init__(self, authenticator: Authenticator):
        self.tsetmc_service = TsetmcService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            sort_by = request.args.get('sort_by', '')
            sort_order = request.args.get('sort_order', 'asc')

            return_info = self.tsetmc_service.get_return_info(sort_order=sort_order, sort_by=sort_by)
            data = defaultdict(lambda: defaultdict(list))

            for obj in return_info:
                if obj.index_type == 'stock':
                    category = 'stock'
                elif obj.index_type == 'بازار':
                    category = 'market'
                elif obj.index_type == 'صنعت':
                    category = 'industrial'
                else:
                    continue  # Skip if not 'سهام' or 'صنعت'

                subcategory = None
                if obj.type == '10 روز':
                    subcategory = '10 روز'
                elif obj.type == '5 روز':
                    subcategory = '5 روز'
                elif obj.type == 'سه ماهه':
                    subcategory = 'سه ماهه'
                elif obj.type == 'شش ماهه':
                    subcategory = 'شش ماهه'
                elif obj.type == 'يک سال':
                    subcategory = 'يک سال'
                elif obj.type == 'يک ماهه':
                    subcategory = 'يک ماهه'

                data[category][subcategory].append({
                    'tse_id': obj.tse_id,
                    'return': obj.return_value,
                    'symbol': obj.symbol,
                    'rank': obj.rank
                })

            self.response = data
            return self.response
        else:
            return self.authenticator.message
