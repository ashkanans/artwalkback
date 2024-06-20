from datetime import datetime
from typing import Type

from sqlalchemy.orm import Session
from werkzeug.security import check_password_hash

from backend.web.model.user import User


class UserDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username: str, email: str, password_hash: str, name: str, sirname: str) -> User:
        user = User(username=username, email=email, password_hash=password_hash, created_at=datetime.now(),
                    notificationIsSet=False, name=name, sirname=sirname)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user_by_id(self, user_id: int) -> Type[User] | None:
        return self.session.query(User).filter_by(user_id=user_id).first()

    def get_user_by_username(self, username: str) -> Type[User] | None:
        return self.session.query(User).filter_by(username=username).first()

    def get_user_by_email(self, email: str) -> Type[User] | None:
        return self.session.query(User).filter_by(email=email).first()

    def update_user(self, user: User, username: str, email: str, password_hash: str, notificationIsSet: bool,
                    last_update: datetime) -> User:
        user.username = username
        user.email = email
        user.password_hash = password_hash
        user.notificationIsSet = notificationIsSet
        user.last_update = last_update
        self.session.commit()
        return user

    def delete_user(self, user: User):
        self.session.delete(user)
        self.session.commit()

    def check_login_credentials(self, provided_username, provided_password):
        try:

            user = self.get_user_by_username(provided_username)

            if user:
                stored_password_hash = user.password_hash
                # Check if the provided password matches the stored hash
                if check_password_hash(stored_password_hash, provided_password):
                    print('Login successful!')
                    return True
                else:
                    print('Incorrect password.')
                    return False
            else:
                print('User not found.')
                return False
        except Exception as e:
            print(f'Error checking login credentials: {e}')
            return False
