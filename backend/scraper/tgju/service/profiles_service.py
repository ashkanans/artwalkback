from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.tgju.dao.profiles_dao import ProfilesDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class ProfilesService:
    def __init__(self):
        """
        Initializes the TgjuProfilesService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.tgju_profiles_dao = ProfilesDao(session)

    def save_tgju_profile(self, data):
        """
        Saves a new tgju profile.

        Parameters:
        - data (dict): Dictionary containing tgju profile data.

        Returns:
        - TgjuProfiles: Saved tgju profile object.
        """
        return self.tgju_profiles_dao.save_tgju_profile(data)

    def get_all_tgju_profiles(self):
        """
        Retrieves all tgju profiles.

        Returns:
        - list: List of all tgju profiles.
        """
        return self.tgju_profiles_dao.get_all_tgju_profiles()

    def get_tgju_profile_by_id(self, tgju_profile_id):
        """
        Retrieves a tgju profile by its ID.

        Parameters:
        - tgju_profile_id (str): Tgju profile ID to retrieve.

        Returns:
        - TgjuProfiles or None: Retrieved tgju profile or None if not found.
        """
        return self.tgju_profiles_dao.get_tgju_profile_by_id(tgju_profile_id)

    def update_tgju_profile(self, data):
        """
        Updates a tgju profile.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - TgjuProfiles or None: Updated tgju profile object or None if not found.
        """
        return self.tgju_profiles_dao.update_tgju_profile(data)

    def delete_tgju_profile(self, tgju_profile_id):
        """
        Deletes a tgju profile by its ID.

        Parameters:
        - tgju_profile_id (str): Tgju profile ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.tgju_profiles_dao.delete_tgju_profile(tgju_profile_id)

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.tgju_profiles_dao.table_exists()

    def create_table(self):
        """
        Create the tgju_profiles table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.tgju_profiles_dao.create_table()

    def get_list_of_symbols(self):
        """
        Retrieves a list of tgju profiles symbols.

        Returns:
        - List or None: Retrieved list of tgju profiles symbols or None if not found.
        """
        return self.tgju_profiles_dao.get_list_of_symbols()

    def get_by_symbol(self, symbol):
        """
        Retrieves a tgju profile by its symbol.

        Parameters:
        - symbol (str): Tgju profile symbol to retrieve.

        Returns:
        - TgjuProfiles or None: Retrieved tgju profile or None if not found.
        """
        return self.tgju_profiles_dao.get_tgju_profile_by_symbol(symbol)

    def update_by_persian_title(self, tgju_symbol, text_content):
        return self.tgju_profiles_dao.update_by_persian_title(tgju_symbol, text_content)

    def update_by_persian_title(self, tgju_symbol, text_content):
        return self.tgju_profiles_dao.update_by_persian_title(tgju_symbol, text_content)

    def get_tgju_profile_by_nameFa(self, nameFa):
        return self.tgju_profiles_dao.get_tgju_profile_by_nameFa(nameFa)
