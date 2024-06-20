from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.client_type_dao import ClientTypeDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class ClientTypeService(BaseLogger):
    def __init__(self):
        """
        Initializes the ClientTypeService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.client_type_dao = ClientTypeDao(session)

    def save_client_type(self, data):
        """
        Saves a new client type  entry.

        Parameters:
        - data (dict): Dictionary containing client type  data.

        Returns:
        - int: Saved client type  entry's inscode
        """
        return self.client_type_dao.save_client_type(data)

    def get_all_client_type_entries(self):
        """
        Retrieves all client type  entries.

        Returns:
        - list: List of all client type  entries.
        """
        return self.client_type_dao.get_all_client_type_entries()

    def get_client_type_by_inscode(self, code):
        """
        Retrieves a client type  entry by its inscode.

        Parameters:
        - code (str): client type  entry inscode to retrieve.

        Returns:
        - ClientType or None: Retrieved client type  entry or None if not found.
        """
        return self.client_type_dao.get_client_type_by_inscode(code)

    def update_client_type(self, data):
        """
        Updates a client type  entry.

        Parameters:
        - code (str): client type  entry inscode to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated client type  entry's inscode
        """

        return self.client_type_dao.update_client_type(data)

    def delete_client_type_by_inscode(self, code):
        """
        Deletes a client type  entry by its inscode.

        Parameters:
        - code (str): client type  entry inscode to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.client_type_dao.delete_client_type_by_inscode(code)

    def create_table(self):
        """
        Create the client type table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.client_type_dao.create_table()

    def table_exists(self):
        """
        Create the client type table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """

        return self.client_type_dao.table_exists()

    def get_list_data(self, inscode):
        return ClientTypeDao.get_list_data(self, inscode)
