from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.ime.dao.producer_groups_dao import ProducerGroupsDao
from backend.scraper.logger.base_logger import BaseLogger

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class ProducerGroupsService(BaseLogger):
    def __init__(self):
        """
        Initializes the ProducerGroupsService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.producer_groups_info_dao = ProducerGroupsDao(session)

    def save_producer_groups_info(self, data):
        """
        Saves a new producer groups info entry.

        Parameters:
        - data (list of dict): List of Dictionary containing updated data.

        Returns:
        - int: Saved producer groups info entry's ID
        """
        return self.producer_groups_info_dao.save_producer_groups_info(data)

    def get_all_producer_groups_info_entries(self):
        """
        Retrieves all producer groups info entries.

        Returns:
        - list: List of all producer groups info entries.
        """
        return self.producer_groups_info_dao.get_all_producer_groups_info_entries()

    def get_producer_groups_info_by_id(self, name):
        """
        Retrieves a producer groups info entry by its ID.

        Parameters:
        - name (str): producer groups info entry ID to retrieve.

        Returns:
        - ProducerGroups or None: Retrieved producer groups info entry or None if not found.
        """
        return self.producer_groups_info_dao.get_producer_groups_info_by_id(name)

    def update_producer_groups_info(self, data):
        """
        Updates a producer groups info entry.

        Parameters:
        - name (str): producer groups info entry ID to update.
        - data (list of dict): List of Dictionary containing updated data.

        Returns:
        - str: Updated producer groups info entry's ID
        """
        result = []
        for item in data:
            result.append({"name": item.get('name'), "code": item.get('code')})

        return self.producer_groups_info_dao.update_producer_groups_info(result)

    def delete_producer_groups_info_by_id(self, name):
        """
        Deletes a producer groups info entry by its ID.

        Parameters:
        - name (str): producer groups info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.producer_groups_info_dao.delete_producer_groups_info_by_id(name)

    def create_table(self):
        """
        Create the producer groups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.producer_groups_info_dao.create_table()

    def get_all_ins_codes(self):
        """
        Retrieves all persian symbols.

        Returns:
        - list: List of all persian symbols.
        """
        return self.producer_groups_info_dao.get_all_ins_codes()

    def table_exists(self):
        """
        Create the producer groups info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.producer_groups_info_dao.table_exists()
