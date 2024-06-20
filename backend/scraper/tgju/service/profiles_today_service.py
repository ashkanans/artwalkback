from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.tgju.dao.profiles_today_dao import ProfilesTodayDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class ProfilesTodayService:
    def __init__(self):
        """
        Initializes the ProfilesTodayService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.profiles_today_dao = ProfilesTodayDao(session)

    def save_profile_today(self, data):
        """
        Saves a new profile today entry.

        Parameters:
        - data (list): List containing profile today data.

        Returns:
        - ProfilesToday: Saved profile today object.
        """
        return self.profiles_today_dao.save_profile_today(data)

    def get_all_profile_todays(self):
        """
        Retrieves all profile today entries.

        Returns:
        - list: List of all profile today entries.
        """
        return self.profiles_today_dao.get_all_profile_todays()

    def get_profile_today_by_key(self, key):
        """
        Retrieves a profile today entry by its Key.

        Parameters:
        - key (str): Key to retrieve.

        Returns:
        - ProfilesToday or None: Retrieved profile today entry or None if not found.
        """
        return self.profiles_today_dao.get_profile_today_by_key(key)

    def update_profile_today(self, data):
        """
        Updates a profile today entry.

        Parameters:
        - data (list): List containing updated data.

        Returns:
        - ProfilesToday or None: Updated profile today entry object or None if not found.
        """
        return self.profiles_today_dao.update_profile_today(data)

    def delete_profile_today(self, key):
        """
        Deletes a profile today entry by its Key.

        Parameters:
        - key (str): Key to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.profiles_today_dao.delete_profile_today(key)

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.profiles_today_dao.table_exists()

    def create_table(self):
        """
        Create the profiles_today table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.profiles_today_dao.create_table()
