from flask import session

from backend.web.dao.artwalk.places_dao import PlacesDAO
from backend.web.dao.artwalk.users_dao import UsersDAO
from backend.web.handlers.api.authenticator import Authenticator
from backend.web.handlers.api.messages import MESSAGES
from backend.web.model.artwalk.places import AWPlaces


class ArtwalkPlacesHandler:
    def __init__(self, authenticator: Authenticator):
        self.places_dao= PlacesDAO()
        self.authenticator = authenticator
        self.response = {"": ""}

    def handle_request(self, request):
        try:

            places_tuple = self.places_dao.read_all_places()
            places_dict = [AWPlaces.from_tuple(single_tuple) for single_tuple in places_tuple[1:2]]

            self.response = places_dict
            return self.response

        except Exception as e:
            self.response = MESSAGES['LOGIN']['ERROR_CHECKING_CREDENTIALS'](e)
            return self.response
