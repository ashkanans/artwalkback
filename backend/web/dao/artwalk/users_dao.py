import hashlib
import sqlite3

from backend.database_config.database_artwalk.config import DB_PATH
from backend.web.model.artwalk.user import AWUsers


class UsersDAO:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name

    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Create users table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL,
                            email TEXT,
                            mobile_phone TEXT,
                            hash_password TEXT
                        )''')

        conn.commit()
        conn.close()

    def insert_user(self, username, mobile_phone, password):
        email = ""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Check if the username already exists
        existing_user = self.get_user_by_username(username)
        if existing_user:
            conn.close()
            return existing_user  # Return existing user if found

        # Hash the password
        hashed_password = self.hash_password(password)

        cursor.execute('''INSERT INTO users (username, email, mobile_phone, hash_password)
                          VALUES (?, ?, ?, ?)''',
                       (username, email, mobile_phone, hashed_password))

        conn.commit()

        # Get the ID of the inserted user
        user_id = cursor.lastrowid

        conn.close()

        # Return the newly inserted user as an AWUsers object
        return AWUsers(user_id, username, email, mobile_phone, hashed_password)

    def hash_password(self, password):
        # Hash the password using SHA-256
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password

    def get_user_by_id(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM users WHERE user_id = ?''', (user_id,))
        user = cursor.fetchone()

        conn.close()

        if user:
            return AWUsers(*user)
        else:
            return None

    def get_all_users(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM users''')
        users = cursor.fetchall()

        conn.close()
        return users

    def update_user(self, user_id, username=None, email=None, mobile_phone=None, hash_password=None):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        update_fields = []
        if username:
            update_fields.append(('username', username))
        if email:
            update_fields.append(('email', email))
        if mobile_phone:
            update_fields.append(('mobile_phone', mobile_phone))
        if hash_password:
            update_fields.append(('hash_password', hash_password))

        update_query = ', '.join([f'{field[0]} = ?' for field in update_fields])
        update_values = [field[1] for field in update_fields]

        cursor.execute('''UPDATE users SET ''' + update_query + ''' WHERE user_id = ?''',
                       (*update_values, user_id))

        conn.commit()
        conn.close()

    def delete_user(self, user_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''DELETE FROM users WHERE user_id = ?''', (user_id,))

        conn.commit()
        conn.close()

    def get_user_by_username(self, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM users WHERE username = ?''', (username,))
        user = cursor.fetchone()

        conn.close()
        if user:
            return AWUsers(*user)
        else:
            return None

    def check_login_credentials(self, username, password):
        user = self.get_user_by_username(username)
        if user is None:
            return False  # User not found

        # Extract the hashed password from the database
        hashed_password_from_db = user.hash_password  # Assuming hash_password is stored at index 4

        # Hash the provided password
        hashed_password_input = self.hash_password(password)

        # Compare the hashed passwords
        if hashed_password_from_db == hashed_password_input:
            return True  # Passwords match
        else:
            return False  # Passwords don't match

    def delete_user_by_username(self, username):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        cursor.execute('''DELETE FROM users WHERE username = ?''', (username,))

        conn.commit()
        conn.close()

