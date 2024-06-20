from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.tgju.dao.profiles_summary_dao import ProfilesSummaryDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class ProfilesSummaryService:
    def __init__(self):
        """
        Initializes the ProfilesSummaryService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.profiles_summary_dao = ProfilesSummaryDao(session)

    def save_profile_summary(self, data):
        """
        Saves a new profile summary.

        Parameters:
        - data (dict): Dictionary containing profile summary data.

        Returns:
        - ProfilesSummary: Saved profile summary object.
        """
        return self.profiles_summary_dao.save_profile_summary(data)

    def get_all_profile_summaries(self):
        """
        Retrieves all profile summaries.

        Returns:
        - list: List of all profile summaries.
        """
        return self.profiles_summary_dao.get_all_profile_summaries()

    def update_profile_summary(self, data):
        """
        Updates a profile summary.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - ProfilesSummary or None: Updated profile summary object or None if not found.
        """
        return self.profiles_summary_dao.update_profile_summary(data)

    def delete_profile_summary(self, profile_summary_id):
        """
        Deletes a profile summary by its ID.

        Parameters:
        - profile_summary_id (str): Profile summary ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.profiles_summary_dao.delete_profile_summary(profile_summary_id)

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.profiles_summary_dao.table_exists()

    def create_table(self):
        """
        Create the profiles_summary table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.profiles_summary_dao.create_table()

    def get_first_price_by_symbol_by_year(self, Symbol, year):
        return self.profiles_summary_dao.get_first_price_by_symbol_by_year(Symbol, year)
