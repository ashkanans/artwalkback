import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.tradingeconomics.dao.profiles_dao import ProfilesDao
from backend.scraper.logger.base_logger import BaseLogger

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class ProfilesService(BaseLogger):
    def __init__(self):
        """
        Initializes the ProfilesService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.profiles_dao = ProfilesDao(session)

    def save_Profiles(self, data):
        """
        Saves a new profiles.

        Parameters:
        - data (dict): Dictionary containing profiles data.

        Returns:
        - Profiles: Saved profiles object.
        """
        return self.profiles_dao.save_profiles(data)

    def get_all_Profiles(self):
        """
        Retrieves all profiles.

        Returns:
        - list: List of all profiles.
        """
        return self.profiles_dao.get_all_profiless()

    def get_all_urls(self):
        """
        Retrieves all profiles urls.

        Returns:
        - list: List of all profiles urls.
        """
        return self.profiles_dao.get_all_urls()


    def update_Profiles(self, data):
        """
        Updates a profiles.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - Profiles or None: Updated profiles object or None if not found.
        """
        return self.profiles_dao.update_profiles(data)

    def update_Profile_by_link(self, data):
        """
        Updates a profiles.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - Profiles or None: Updated profiles object or None if not found.
        """
        return self.profiles_dao.update_Profile_by_link(data)


    def delete_Profiles(self, name):
        """
        Deletes a profiles by its tracing number.

        Parameters:
        - tracing_no (int): Tracing number to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.profiles_dao.delete_profiles(name)

    def create_table(self):
        """
        Create the profiles table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.profiles_dao.create_table()

    def table_exists(self):
        """
        Create the instrument_info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.profiles_dao.table_exists()
