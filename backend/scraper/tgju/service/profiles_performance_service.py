from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.tgju.dao.profiles_performance_dao import ProfilesPerformanceDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class ProfilesPerformanceService:
    def __init__(self):
        """
        Initializes the ProfilesPerformanceService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.profiles_performance_dao = ProfilesPerformanceDao(session)

    def save_performance_profile(self, data):
        """
        Saves a new performance profile.

        Parameters:
        - data (dict): Dictionary containing performance profile data.

        Returns:
        - ProfilesPerformance: Saved performance profile object.
        """
        return self.profiles_performance_dao.save_performance_profile(data)

    def get_all_performance_profiles(self):
        """
        Retrieves all performance profiles.

        Returns:
        - list: List of all performance profiles.
        """
        return self.profiles_performance_dao.get_all_performance_profiles()

    def get_performance_profile_by_symbol(self, symbol):
        """
        Retrieves a performance profile by its Symbol.

        Parameters:
        - symbol (str): Symbol to retrieve.

        Returns:
        - ProfilesPerformance or None: Retrieved performance profile or None if not found.
        """
        return self.profiles_performance_dao.get_performance_profile_by_symbol(symbol)

    def update_performance_profile(self, data):
        """
        Updates a performance profile.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - ProfilesPerformance or None: Updated performance profile object or None if not found.
        """
        return self.profiles_performance_dao.update_performance_profile(data)

    def delete_performance_profile(self, symbol):
        """
        Deletes a performance profile by its Symbol.

        Parameters:
        - symbol (str): Symbol to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.profiles_performance_dao.delete_performance_profile(symbol)

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.profiles_performance_dao.table_exists()

    def create_table(self):
        """
        Create the profiles_performance table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.profiles_performance_dao.create_table()
