from flask import Request
from backend.web.handlers.api.authenticator import Authenticator
from backend.web.service.new_ime import NewImeService


class CommodityImeSubCategoryGroupsHandler:
    def __init__(self, authenticator: Authenticator):
        self.imeService = NewImeService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request: Request):
        self.authenticator.token_authenticator(request)
        if self.authenticator.authorized:
            sort_by = request.args.get('sort_by', '')
            sort_order = request.args.get('sort_order', 'asc')
            sub_category_groups = self.imeService.get_sub_category_groups(sort_by=sort_by.capitalize(), sort_order=sort_order);

            data = [{"name": sub_category.Name, "code": sub_category.code} for sub_category in sub_category_groups]

            self.response = {'data': data}
            return self.response
        else:
            return self.authenticator.message
