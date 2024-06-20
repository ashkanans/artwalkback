from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from backend.database_config.config import SQL_SERVER_URL
from backend.web.dao.user import UserDAO
from backend.web.model.user import User
from backend.web.service.configuration.service import ConfigurationService


# Creating the SQLAlchemy engine


class UserService:

    def __init__(self):

        self.configuration_service = ConfigurationService()
        self.engine = create_engine(SQL_SERVER_URL)
        self.Session = sessionmaker(bind=self.engine)
        session = self.Session()
        self.user_dao = UserDAO(session)

    def create_user(self, username: str, email: str, password: str, name: str, sirname: str) -> User:
        password_hash = generate_password_hash(password)
        new_user = self.user_dao.create_user(username, email, password_hash, name, sirname)
        if new_user:
            self.configuration_service.insert_stock_table_configurations_for_user(username)
        return new_user

    def get_user_by_id(self, user_id: int) -> User:
        return self.user_dao.get_user_by_id(user_id)

    def get_user_by_username(self, username: str) -> User:
        return self.user_dao.get_user_by_username(username)

    def get_user_by_email(self, email: str) -> User:
        return self.user_dao.get_user_by_email(email)

    def update_user(self, user_id: int, username: str, email: str, password_hash: str, notificationIsSet,
                    last_update) -> User:
        user = self.get_user_by_id(user_id)
        if user:
            return self.user_dao.update_user(user, username, email, password_hash, notificationIsSet, last_update)
        return None

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            self.configuration_service.delete_stock_table_configurations_for_user(user.username)
            self.user_dao.delete_user(user)

    def check_login_credentials(self, provided_username, provided_password):
        return self.user_dao.check_login_credentials(provided_username, provided_password)

    def delete_user_by_username(self, username):
        user = self.get_user_by_username(username)
        if user:
            self.user_dao.delete_user(user)
