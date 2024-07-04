import os

from flask import session

from backend.web.dao.artwalk.places_dao import PlacesDAO
from backend.web.dao.artwalk.users_dao import UsersDAO
from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES
from backend.web.model.artwalk.places import AWPlaces


class ArtwalkPredictHandler:
    def __init__(self, authenticator: Authenticator):
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request):
        try:
            cwd = os.getcwd()
            self.response = {"current_working_directory": cwd}
            return self.response

        except Exception as e:
            self.response = MESSAGES['LOGIN']['ERROR_CHECKING_CREDENTIALS'](e)
            return self.response
