from flask import abort

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES
from backend.web.service.user import UserService


class SignupHandler:
    def __init__(self, authenticator: Authenticator):
        self.user_service = UserService()
        self.authenticator = authenticator

    def handle_request(self, request):
        try:
            data = request.get_json()
            username = data['username']
            email = data['email']
            password = data['password']
            name = data['name']
            sirname = data['sirname']
            if username is None or password is None:
                abort(400)

            if self.user_service.get_user_by_username(username):
                return MESSAGES['REGISTRATION']['USER_ALREADY_EXISTS'](username)

            self.user_service.create_user(username, email, password, name, sirname)

            return MESSAGES['AUTHENTICATION']['REGISTRATION_SUCCESSFUL']
        except Exception as e:
            return MESSAGES['REGISTRATION']['ERROR_REGISTERING_USER'](e)
