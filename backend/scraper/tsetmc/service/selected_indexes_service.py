from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.selected_indexes_dao import SelectedIndexesDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class SelectedIndexesService(BaseLogger):
    def __init__(self):
        """
        Initializes the SelectedIndexesService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.selected_indexes_dao = SelectedIndexesDao(session)

    def save_selected_indexes(self, data):
        """
        Saves a new selected indexes.

        Parameters:
        - data (dict): Dictionary containing selected indexes data.

        Returns:
        - SelectedIndexes: Saved selected indexes object.
        """
        return self.selected_indexes_dao.save_selected_indexes(data)

    def get_all_selected_indexess(self):
        """
        Retrieves all selected indexess.

        Returns:
        - list: List of all selected indexess.
        """
        return self.selected_indexes_dao.get_all_selected_indexess()

    def get_selected_indexes_by_name(self, selected_indexes_name):
        """
        Retrieves a selected indexes by its ID.

        Parameters:
        - selected_indexes_id (int): selected indexes ID to retrieve.

        Returns:
        - SelectedIndexes or None: Retrieved selected indexes or None if not found.
        """
        return self.selected_indexes_dao.get_selected_indexes_by_name(selected_indexes_name)

    def update_selected_indexes(self, data):
        """
        Updates a selected indexes.

        Parameters:
        - selected_indexes_id (int): selected indexes ID to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - SelectedIndexes or None: Updated selected indexes object or None if not found.
        """
        return self.selected_indexes_dao.update_selected_indexes(data)

    def delete_selected_indexes(self, selected_indexes_name):
        """
        Deletes a selected indexes by its ID.

        Parameters:
        - selected_indexes_id (int): selected indexes ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.selected_indexes_dao.delete_selected_indexes(selected_indexes_name)

    def create_table(self):
        """
        Create the selected_indexes table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.selected_indexes_dao.create_table()

    def table_exists(self):
        """
        Create the selected_indexes table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.selected_indexes_dao.table_exists()
