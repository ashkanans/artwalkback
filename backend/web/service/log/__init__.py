from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from backend.database_config.config import SQL_SERVER_URL
from backend.web.dao.log.log import LogDAO
from backend.web.model.Log.log import Log

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class LogService:
    def __init__(self):
        self.log_dao = LogDAO(session)

    def create_log(self, endpoint: str, http_method: str, client_ip: str) -> Log:
        return self.log_dao.create_log(endpoint=endpoint, http_method=http_method, client_ip=client_ip)

    def get_log_by_id(self, log_id: int) -> Type[Log] | None:
        return self.log_dao.get_log_by_id(log_id)

    # def update_log(self, user_id: int, username: str, email: str, password_hash: str, notificationIsSet,
    #                 last_update) -> User:
    #     user = self.get_user_by_id(user_id)
    #     if user:
    #         return self.user_dao.update_user(user, username, email, password_hash, notificationIsSet, last_update)
    #     return None

    def delete_log(self, log_id: int):
        log = self.get_log_by_id(log_id)
        if log:
            self.log_dao.delete_log(log)
