from flask import session

from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES
from backend.web.service.user import UserService


class AuthenticateHandler:
    def __init__(self, authenticator: Authenticator):
        self.user_service = UserService()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request):
        try:
            data = request.get_json()
            username = data['username']
            password = data['password']

            user = self.user_service.get_user_by_username(username)
            result = self.user_service.check_login_credentials(username, password)
            if result:
                session['username'] = username
                token = self.authenticator.generate_auth_token(user_id=user.user_id, username=user.username)

                user_info = {'id': user.user_id,
                             'name': user.name,
                             'sirname': user.sirname,
                             'notificationIsSet': user.notificationIsSet}
                self.response = MESSAGES['LOGIN']['AUTHENTICATION_SUCCESSFUL'](token, username, user_info)
                return self.response
            else:
                self.response = MESSAGES['AUTHENTICATION']['NOT_AUTHORIZED']
                return self.response
        except Exception as e:
            self.response = MESSAGES['LOGIN']['ERROR_CHECKING_CREDENTIALS'](e)
            return self.response
