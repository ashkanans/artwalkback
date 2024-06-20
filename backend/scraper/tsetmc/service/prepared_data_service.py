from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.prepared_data_dao import PreparedDataDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class PreparedDataService(BaseLogger):
    def __init__(self):
        """
        Initializes the PreparedDataService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.prepared_data_dao = PreparedDataDao(session)

    def save_prepared_data(self, data):
        """
        Saves a new Prepared Data  entry.

        Parameters:
        - data (dict): Dictionary containing Prepared Data  data.

        Returns:
        - int: Saved Prepared Data  entry's tseMsgIdn
        """
        return self.prepared_data_dao.save_prepared_data(data)

    def get_all_prepared_data_entries(self):
        """
        Retrieves all Prepared Data  entries.

        Returns:
        - list: List of all Prepared Data  entries.
        """
        return self.prepared_data_dao.get_all_prepared_data_entries()

    def get_prepared_data_by_Id(self, code):
        """
        Retrieves a Prepared Data  entry by its tseMsgIdn.

        Parameters:
        - code (str): Prepared Data  entry tseMsgIdn to retrieve.

        Returns:
        - PreparedData or None: Retrieved Prepared Data  entry or None if not found.
        """
        return self.prepared_data_dao.get_prepared_data_by_id(code)

    def update_prepared_data(self, data):
        """
        Updates a Prepared Data  entry.

        Parameters:
        - code (str): Prepared Data  entry tseMsgIdn to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated Prepared Data  entry's tseMsgIdn
        """

        return self.prepared_data_dao.update_prepared_data(data)

    def delete_prepared_data_by_tseMsgId(self, code):
        """
        Deletes a Prepared Data  entry by its tseMsgIdn.

        Parameters:
        - code (str): Prepared Data  entry tseMsgIdn to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.prepared_data_dao.delete_prepared_data_by_id(code)

    def create_table(self):
        """
        Create the Prepared Data table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.prepared_data_dao.create_table()

    def table_exists(self):
        """
        Create the Prepared Data table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """

        return self.prepared_data_dao.table_exists()
