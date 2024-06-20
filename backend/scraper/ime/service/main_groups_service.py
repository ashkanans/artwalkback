from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.ime.dao.main_groups_dao import MainGroupsDao
from backend.scraper.logger.base_logger import BaseLogger

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class MainGroupsService(BaseLogger):
    def __init__(self):
        """
        Initializes the MainGroupsService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.main_groups_info_dao = MainGroupsDao(session)

    def save_main_groups_info(self, data):
        """
        Saves a new main groups info entry.

        Parameters:
        - data (dict): Dictionary containing main groups info data.

        Returns:
        - int: Saved main groups info entry's ID
        """
        return self.main_groups_info_dao.save_main_groups_info(data)

    def get_all_main_groups_info_entries(self):
        """
        Retrieves all main groups info entries.

        Returns:
        - list: List of all main groups info entries.
        """
        return self.main_groups_info_dao.get_all_main_groups_info_entries()

    def get_main_groups_info_by_id(self, code):
        """
        Retrieves a main groups info entry by its ID.

        Parameters:
        - code (str): main groups info entry ID to retrieve.

        Returns:
        - MainGroups or None: Retrieved main groups info entry or None if not found.
        """
        return self.main_groups_info_dao.get_main_groups_info_by_id(code)

    def update_main_groups_info(self, data):
        """
        Updates a main groups info entry.

        Parameters:
        - code (str): main groups info entry ID to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated main groups info entry's ID
        """
        result = []
        for item in data:
            result.append({"Name": item.get('Name'), "code": item.get('code')})
        return self.main_groups_info_dao.update_main_groups_info(result)

    def delete_main_groups_info_by_id(self, code):
        """
        Deletes a main groups info entry by its ID.

        Parameters:
        - code (str): main groups info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.main_groups_info_dao.delete_main_groups_info_by_id(code)

    def create_table(self):
        """
        Create the main groups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.main_groups_info_dao.create_table()

    def table_exists(self):
        """
        Create the main groups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """

        return self.main_groups_info_dao.table_exists()
