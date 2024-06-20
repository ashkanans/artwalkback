from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.all_indexes_dao import AllIndexesDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class AllIndexesService(BaseLogger):
    def __init__(self):
        """
        Initializes the AllIndexesService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.all_indexes_dao = AllIndexesDao(session)

    def save_all_indexes(self, data):
        """
        Saves a new all indexes.

        Parameters:
        - data (dict): Dictionary containing all indexes data.

        Returns:
        - AllIndexes: Saved all indexes object.
        """
        return self.all_indexes_dao.save_all_indexes(data)

    def get_all_all_indexess(self):
        """
        Retrieves all all indexess.

        Returns:
        - list: List of all all indexess.
        """
        return self.all_indexes_dao.get_all_all_indexess()

    def get_all_indexes_by_name(self, all_indexes_name):
        """
        Retrieves a all indexes by its ID.

        Parameters:
        - all_indexes_id (int): all indexes ID to retrieve.

        Returns:
        - AllIndexes or None: Retrieved all indexes or None if not found.
        """
        return self.all_indexes_dao.get_all_indexes_by_name(all_indexes_name)

    def update_all_indexes(self, data):
        """
        Updates all indexes.

        Parameters:
        - all_indexes_id (int): all indexes ID to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - AllIndexes or None: Updated all indexes object or None if not found.
        """
        return self.all_indexes_dao.update_all_indexes(data)

    def delete_all_indexes(self, all_indexes_name):
        """
        Deletes a all indexes by its ID.

        Parameters:
        - all_indexes_id (int): all indexes ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.all_indexes_dao.delete_all_indexes(all_indexes_name)

    def create_table(self):
        """
        Create the all_indexes table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.all_indexes_dao.create_table()

    def table_exists(self):
        """
        Create the all_indexes table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.all_indexes_dao.table_exists()

    def get_data_contain_specifi_value_in_name(self, txt):
        return self.all_indexes_dao.get_data_contain_specifi_value_in_name(txt)
