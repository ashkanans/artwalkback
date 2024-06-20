from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.get_trade_dao import GetTradeDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class GetTradeService(BaseLogger):
    def __init__(self):
        """
        Initializes the GetTradeService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.get_trade_dao = GetTradeDao(session)

    def save_get_trade(self, data):
        """
        Saves a new get trade  entry.

        Parameters:
        - data (dict): Dictionary containing get trade  data.

        Returns:
        - int: Saved get trade  entry's tseMsgIdn
        """
        return self.get_trade_dao.save_get_trade(data)

    def get_all_get_trade_entries(self):
        """
        Retrieves all get trade  entries.

        Returns:
        - list: List of all get trade  entries.
        """
        return self.get_trade_dao.get_all_get_trade_entries()

    def get_get_trade_by_Id(self, code):
        """
        Retrieves a get trade  entry by its tseMsgIdn.

        Parameters:
        - code (str): get trade  entry tseMsgIdn to retrieve.

        Returns:
        - GetTrade or None: Retrieved get trade  entry or None if not found.
        """
        return self.get_trade_dao.get_get_trade_by_id(code)

    def update_get_trade(self, data):
        """
        Updates a get trade  entry.

        Parameters:
        - code (str): get trade  entry tseMsgIdn to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated get trade  entry's tseMsgIdn
        """

        return self.get_trade_dao.update_get_trade(data)

    def delete_get_trade_by_tseMsgId(self, code):
        """
        Deletes a get trade  entry by its tseMsgIdn.

        Parameters:
        - code (str): get trade  entry tseMsgIdn to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.get_trade_dao.delete_get_trade_by_id(code)

    def create_table(self):
        """
        Create the get trade table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.get_trade_dao.create_table()

    def table_exists(self):
        """
        Create the get trade table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """

        return self.get_trade_dao.table_exists()
