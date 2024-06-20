from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.tgju.dao.profiles_current_dao import CurrentProfilesDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class CurrentProfilesService:
    def __init__(self):
        """
        Initializes the TgjuCurrentProfilesService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.tgju_current_profiles_dao = CurrentProfilesDao(session)

    def save_tgju_current_profile(self, data):
        """
        Saves a new tgju current profile.

        Parameters:
        - data (dict): Dictionary containing tgju current profile data.

        Returns:
        - TgjuCurrentProfiles: Saved tgju current profile object.
        """
        return self.tgju_current_profiles_dao.save_tgju_current_profile(data)

    def get_all_tgju_current_profiles(self):
        """
        Retrieves all tgju current profiles.

        Returns:
        - list: List of all tgju current profiles.
        """
        return self.tgju_current_profiles_dao.get_all_tgju_current_profiles()

    def get_tgju_current_profile_by_id(self, tgju_current_profile_id):
        """
        Retrieves a tgju current profile by its ID.

        Parameters:
        - tgju_current_profile_id (str): Tgju current profile ID to retrieve.

        Returns:
        - TgjuCurrentProfiles or None: Retrieved tgju current profile or None if not found.
        """
        return self.tgju_current_profiles_dao.get_tgju_current_profile_by_id(tgju_current_profile_id)

    def update_tgju_current_profile(self, data):
        """
        Updates a tgju current profile.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - TgjuCurrentProfiles or None: Updated tgju current profile object or None if not found.
        """
        return self.tgju_current_profiles_dao.update_tgju_current_profile(data)

    def delete_tgju_current_profile(self, tgju_current_profile_id):
        """
        Deletes a tgju current profile by its ID.

        Parameters:
        - tgju_current_profile_id (str): Tgju current profile ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.tgju_current_profiles_dao.delete_tgju_current_profile(tgju_current_profile_id)

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.tgju_current_profiles_dao.table_exists()

    def create_table(self):
        """
        Create the tgju_current_profiles table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.tgju_current_profiles_dao.create_table()

    def get_tgju_current_profile_by_symbol(self, symbol):
        return self.tgju_current_profiles_dao.get_tgju_current_profile_by_symbol(symbol)
