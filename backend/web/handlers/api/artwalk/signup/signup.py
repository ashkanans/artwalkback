from flask import abort

from backend.web.dao.artwalk.users_dao import UsersDAO
from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES


class ArtwalkSignupHandler:
    def __init__(self, authenticator: Authenticator):
        self.user_dao = UsersDAO()
        self.authenticator = authenticator

    def handle_request(self, request):
        try:
            data = request.get_json()
            username = data['username']
            mobile_number = data['mobile_number']
            password = data['password']
            if username is None or password is None:
                abort(400)

            if self.user_dao.get_user_by_username(username):
                return MESSAGES['REGISTRATION']['USER_ALREADY_EXISTS'](username)

            self.user_dao.insert_user(username, mobile_number, password)

            return MESSAGES['AUTHENTICATION']['REGISTRATION_SUCCESSFUL']
        except Exception as e:
            return MESSAGES['REGISTRATION']['ERROR_REGISTERING_USER'](e)
