from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.tgju.dao.profiles_at_a_glance_dao import ProfilesAtAGlanceDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class ProfilesAtAGlanceService:
    def __init__(self):
        """
        Initializes the ProfilesAtAGlanceService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.profiles_at_a_glance_dao = ProfilesAtAGlanceDao(session)

    def save_profile_at_a_glance(self, data):
        """
        Saves a new profile at a glance.

        Parameters:
        - data (dict): Dictionary containing profile at a glance data.

        Returns:
        - ProfilesAtAGlance: Saved profile at a glance object.
        """
        return self.profiles_at_a_glance_dao.save_profile_at_a_glance(data)

    def get_all_profiles_at_a_glance(self):
        """
        Retrieves all profiles at a glance.

        Returns:
        - list: List of all profiles at a glance.
        """
        return self.profiles_at_a_glance_dao.get_all_profiles_at_a_glance()

    def get_profile_at_a_glance_by_id(self, profile_id):
        """
        Retrieves a profile at a glance by its ID.

        Parameters:
        - profile_id (str): Profile at a glance ID to retrieve.

        Returns:
        - ProfilesAtAGlance or None: Retrieved profile at a glance or None if not found.
        """
        return self.profiles_at_a_glance_dao.get_profile_at_a_glance_by_id(profile_id)

    def update_profile_at_a_glance(self, data):
        """
        Updates a profile at a glance.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - ProfilesAtAGlance or None: Updated profile at a glance object or None if not found.
        """
        return self.profiles_at_a_glance_dao.update_profile_at_a_glance(data)

    def delete_profile_at_a_glance(self, profile_id):
        """
        Deletes a profile at a glance by its ID.

        Parameters:
        - profile_id (str): Profile at a glance ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.profiles_at_a_glance_dao.delete_profile_at_a_glance(profile_id)

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.profiles_at_a_glance_dao.table_exists()

    def create_table(self):
        """
        Create the profiles_at_a_glance table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.profiles_at_a_glance_dao.create_table()
