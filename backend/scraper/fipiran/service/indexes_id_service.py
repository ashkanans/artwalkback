from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.fipiran.dao.indexes_id_dao import IndexesIdDao
from backend.scraper.logger.base_logger import BaseLogger

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class IndexesIdService(BaseLogger):
    def __init__(self):
        """
        Initializes the IndexesIdService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.index_id_dao = IndexesIdDao(session)

    def save_indexes_id(self, data):
        """
        Saves a new index id.

        Parameters:
        - data (dict): Dictionary containing index data.

        Returns:
        - int: Saved index's InstrumentID.
        """
        return self.index_id_dao.save_indexes_id(data)

    def get_all_indexes_id(self):
        """
        Retrieves all indices id.

        Returns:
        - list: List of all indices id.
        """
        return self.index_id_dao.get_all_indexes_id()

    def get_indexes_id_by_key(self, index_id):
        """
        Retrieves an index by its InstrumentID.

        Parameters:
        - index_id (int): Index InstrumentID to retrieve.

        Returns:
        - Index or None: Retrieved index or None if not found.
        """
        return self.index_id_dao.get_indexes_id_by_key(index_id)

    def update_indexes_id(self, data):
        """
        Updates an index id.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - int: Updated index's InstrumentID.
        """
        return self.index_id_dao.update_indexes_id(data)

    def delete_indexes_id_by_key(self, index_id):
        """
        Deletes an index by its InstrumentID.

        Parameters:
        - index_id (int): Index InstrumentID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.index_id_dao.delete_indexes_id_by_key(index_id)

    def create_table(self):
        """
        Create the index table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.index_id_dao.create_table()

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.index_id_dao.table_exists()

    def get_by_InstrumentID(self, index_id):
        """
        Retrieves an index by its name and date of issue.

        Parameters:
        - InstrumentID (str): Index id


        Returns:
        - Index or None: Retrieved index or None if not found.
        """
        return self.index_id_dao.get_by_InstrumentID(index_id)
