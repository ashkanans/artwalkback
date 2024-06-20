from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.codal_announcement_dao import CodalAnnouncementDao


class CodalAnnouncementService(BaseLogger):
    def __init__(self, dynamic_tablename):
        """
        Initializes the CodalAnnouncementService.

        Parameters:
        - session: SQLAlchemy session object
        """

        # Creating the SQLAlchemy engine
        self.engine = create_engine(SQL_SERVER_URL)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.codal_announcement_dao = CodalAnnouncementDao(self.session, self.engine, dynamic_tablename)

    def save_codal_announcement(self, data):
        """
        Saves a new codal_announcement entry.

        Parameters:
        - data (dict): Dictionary containing codal_announcement data.

        Returns:
        - int: Saved codal_announcement entry's ID
        """
        return self.codal_announcement_dao.save_codal_announcement(data)

    def get_all_codal_announcements(self):
        """
        Retrieves all codal_announcement entries.

        Returns:
        - list: List of all codal_announcement entries.
        """
        return self.codal_announcement_dao.get_all_codal_announcement()

    def get_recent_codal_announcements(self):
        """
        Retrieves all codal_announcement entries.

        Returns:
        - list: List of all codal_announcement entries.
        """
        return self.codal_announcement_dao.get_recent_codal_announcements()

    def get_codal_announcement_by_id(self, codal_announcement_id):
        """
        Retrieves a codal_announcement entry by its ID.

        Parameters:
        - codal_announcement_id (int): ID of the codal_announcement entry to retrieve.

        Returns:
        - codal_announcementModel or None: Retrieved codal_announcement entry or None if not found.
        """
        return self.codal_announcement_dao.get_codal_announcement_by_id(codal_announcement_id)

    def update_codal_announcement(self, data):
        """
        Updates a codal_announcement entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - int: Updated codal_announcement entry's ID
        """
        cleaned_data = {key: str(value).replace('"', '').replace("'", '') for key, value in data.items()}
        return self.codal_announcement_dao.update_codal_announcement(cleaned_data)

    def delete_codal_announcement_by_id(self, codal_announcement_id):
        """
        Deletes a codal_announcement entry by its ID.

        Parameters:
        - codal_announcement_id (int): ID of the codal_announcement entry to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.codal_announcement_dao.delete_codal_announcement_by_id(codal_announcement_id)

    def create_table(self):
        """
        Create the codal_announcement_table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.codal_announcement_dao.create_table()

    def table_exists(self):
        """
        Create the codal_announcement_table table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.codal_announcement_dao.table_exists()
