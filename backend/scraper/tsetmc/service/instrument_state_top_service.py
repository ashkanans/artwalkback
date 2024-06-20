from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.instrument_state_top_dao import InstrumentStateTopDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class InstrumentStateTopService(BaseLogger):
    def __init__(self):
        """
        Initializes the InstrumentStateTopService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.instrument_state_top_dao = InstrumentStateTopDao(session)

    def save_instrument_state_top(self, data):
        """
        Saves a new Instrument State Top  entry.

        Parameters:
        - data (dict): Dictionary containing Instrument State Top  data.

        Returns:
        - int: Saved Instrument State Top  entry's tseMsgIdn
        """
        return self.instrument_state_top_dao.save_instrument_state_top(data)

    def get_all_instrument_state_top_entries(self):
        """
        Retrieves all Instrument State Top  entries.

        Returns:
        - list: List of all Instrument State Top  entries.
        """
        return self.instrument_state_top_dao.get_all_instrument_state_top_entries()

    def get_instrument_state_top_by_tseMsgIdn(self, code):
        """
        Retrieves a Instrument State Top  entry by its tseMsgIdn.

        Parameters:
        - code (str): Instrument State Top  entry tseMsgIdn to retrieve.

        Returns:
        - InstrumentStateTop or None: Retrieved Instrument State Top  entry or None if not found.
        """
        return self.instrument_state_top_dao.get_instrument_state_top_by_tseMsgIdn(code)

    def update_instrument_state_top(self, data):
        """
        Updates a Instrument State Top  entry.

        Parameters:
        - code (str): Instrument State Top  entry tseMsgIdn to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated Instrument State Top  entry's tseMsgIdn
        """

        return self.instrument_state_top_dao.update_instrument_state_top(data)

    def delete_instrument_state_top_by_tseMsgIdn(self, code):
        """
        Deletes a Instrument State Top  entry by its tseMsgIdn.

        Parameters:
        - code (str): Instrument State Top  entry tseMsgIdn to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.instrument_state_top_dao.delete_instrument_state_top_by_idn(code)

    def create_table(self):
        """
        Create the Instrument State Top table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.instrument_state_top_dao.create_table()

    def table_exists(self):
        """
        Create the Instrument State Top table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """

        return self.instrument_state_top_dao.table_exists()
