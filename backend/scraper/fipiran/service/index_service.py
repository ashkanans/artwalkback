from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.fipiran.dao.index_dao import IndexDao
from backend.scraper.logger.base_logger import BaseLogger

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class IndexService(BaseLogger):
    def __init__(self):
        """
        Initializes the IndexService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.index_dao = IndexDao(session)

    def save_index(self, data):
        """
        Saves a new index.

        Parameters:
        - data (dict): Dictionary containing index data.

        Returns:
        - int: Saved index's ID.
        """
        return self.index_dao.save_index(data)

    def get_all_indices(self):
        """
        Retrieves all indices.

        Returns:
        - list: List of all indices.
        """
        return self.index_dao.get_all_indices()

    def get_index_by_id(self, index_id):
        """
        Retrieves an index by its ID.

        Parameters:
        - index_id (int): Index ID to retrieve.

        Returns:
        - Index or None: Retrieved index or None if not found.
        """
        return self.index_dao.get_index_by_id(index_id)

    def update_index(self, data):
        """
        Updates an index.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - int: Updated index's ID.
        """
        return self.index_dao.update_index(data)

    def delete_index(self, index_id):
        """
        Deletes an index by its ID.

        Parameters:
        - index_id (int): Index ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.index_dao.delete_index_by_id(index_id)

    def create_table(self):
        """
        Create the index table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.index_dao.create_table()

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.index_dao.table_exists()

    def get_by_nameFa(self, nameFa):
        return self.index_dao.get_by_nameFa(nameFa)

    def get_index_by_sectorCode(self, sector_code):
        return self.index_dao.get_index_by_sectorCode(sector_code)
