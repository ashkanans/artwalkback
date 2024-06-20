from flask import session

from backend.web.dao.artwalk.users_dao import UsersDAO
from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES


class ArtwalkAuthenticateHandler:
    def __init__(self, authenticator: Authenticator):
        self.user_dao = UsersDAO()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request):
        try:
            data = request.get_json()
            username = data['username']
            password = data['password']

            user = self.user_dao.get_user_by_username(username)
            result = self.user_dao.check_login_credentials(username, password)
            if result:
                session['username'] = username
                token = self.authenticator.generate_auth_token(user_id=user.user_id, username=user.username)

                user_info = {'id': user.user_id,
                             'mobile_phone': user.mobile_phone
                             }
                self.response = MESSAGES['LOGIN']['AUTHENTICATION_SUCCESSFUL'](token, username, user_info)
                return self.response
            else:
                self.response = MESSAGES['AUTHENTICATION']['NOT_AUTHORIZED']
                return self.response
        except Exception as e:
            self.response = MESSAGES['LOGIN']['ERROR_CHECKING_CREDENTIALS'](e)
            return self.response
