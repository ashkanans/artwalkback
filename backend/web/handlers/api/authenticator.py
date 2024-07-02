import datetime

import jwt
from flask import Request

from backend.web.dao.artwalk.users_dao import UsersDAO
from backend.web.handlers.api.messages import MESSAGES

app_secret_key = b'_5#y2L"F4Q8z\n\xec]/'


class Authenticator:
    def __init__(self):
        self._username = None
        self._user_id = None
        self._token_based_authenticator = None
        self._username_password_based_authenticator = None
        self._authorized = None
        self._message = None

    def token_authenticator(self, request: Request):
        self._token_based_authenticator = True

        token = request.headers.get('Authorization')
        if not token:
            self._message = MESSAGES['AUTHENTICATION']['TOKEN_NOT_FOUND']
            return

        token = token.split(" ")[-1]

        self._authorized, self._username, self._user_id = self.verify_auth_token(token)

        if self.authorized:
            self._message = MESSAGES['AUTHENTICATION']['AUTHORIZED']
        else:
            self._message = MESSAGES['AUTHENTICATION']['NOT_AUTHORIZED']

    def aw_verify_auth_token(self, token):
        try:
            token_payload = jwt.decode(token, app_secret_key, algorithms=['HS256'])
            user_id = token_payload.get('id')
            username = token_payload.get('username')
            if user_id:
                user = UsersDAO().get_user_by_id(user_id)
                if user:
                    return user.username == username, username, user_id
        except jwt.ExpiredSignatureError as e:
            return False, None, None
        except jwt.InvalidTokenError as e:
            return False, None, None
        except Exception as e:
            return False, None, None

    def verify_auth_token(self, token):
        try:
            token_payload = jwt.decode(token, app_secret_key, algorithms=['HS256'])
            user_id = token_payload.get('id')
            username = token_payload.get('username')
            if user_id:
                user = False
                # user = self.user_service.get_user_by_id(user_id)
                if user:
                    return True
        except jwt.ExpiredSignatureError as e:
            return False, None, None
        except jwt.InvalidTokenError as e:
            return False, None, None
        except Exception as e:
            return False, None, None

    def generate_auth_token(self, user_id, username):
        token_payload = {'id': user_id, 'username': username,
                         "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=10)}
        token = jwt.encode(
            token_payload, app_secret_key, algorithm="HS256"
        )
        return token

    @property
    def token_based_authenticator(self):
        return self._token_based_authenticator

    @property
    def username_password_based_authenticator(self):
        return self._username_password_based_authenticator

    @property
    def authorized(self):
        return self._authorized

    @property
    def username(self):
        return self._username

    @property
    def user_id(self):
        return self._user_id

    @property
    def message(self):
        return self._message
