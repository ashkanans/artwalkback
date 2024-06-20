from collections import defaultdict

from flask import Request

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.tsetmc.service import TsetmcService


class TsetmcEnteredmoneyHandler:
    def __init__(self, authenticator: Authenticator):
        self.tsetmc_service = TsetmcService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)

        if self.authenticator.authorized:
            sort_by = request.args.get('sort_by', '')
            sort_order = request.args.get('sort_order', 'asc')

            entered_money = self.tsetmc_service.get_entered_money(sort_order=sort_order, sort_by=sort_by)
            data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

            for obj in entered_money:
                if obj.type_report == 'سهام':
                    category = 'stock'
                elif obj.type_report == 'صنعت':
                    category = 'industry'
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

                if obj.type_rank == 'بيشترين ورود پول حقيقي':
                    key = 'high_enter_money'
                else:
                    key = 'high_exit_money'

                data[category][key][subcategory].append({
                    'tse_id': obj.tse_id,
                    'entered_money': obj.entered_money,
                    'rank': obj.rank,
                    'type_rank': obj.type_rank,
                    'Persian_symbol': obj.Persian_symbol,
                    'type_report': obj.type_report
                })

            self.response = data
            return self.response
        else:
            return self.authenticator.message
