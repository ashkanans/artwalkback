import datetime
from typing import Type

from sqlalchemy.orm import Session
from backend.web.model.Log.log import Log


class LogDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_log(self, client_ip: str, endpoint: str, http_method: str) -> Log:
        new_log = Log(timestamp=datetime.datetime.now(), client_ip=client_ip, endpoint=endpoint, http_method=http_method)
        self.session.add(new_log)
        self.session.commit()
        return new_log

    def get_log_by_id(self, log_id: int) -> Type[Log] | None:
        return self.session.query(Log).filter_by(log_id=log_id).first()

    # def update_log(self, user: User, username: str, email: str, password_hash: str, notificationIsSet: bool,
    #                last_update: datetime) -> User:
    #     user.username = username
    #     user.email = email
    #     user.password_hash = password_hash
    #     user.notificationIsSet = notificationIsSet
    #     user.last_update = last_update
    #     self.session.commit()
    #     return user

    def delete_log(self, log: Log):
        self.session.delete(log)
        self.session.commit()
