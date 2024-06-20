from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.top_trade_most_visited_dao import TradeTopMostVisitedDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class TradeTopService(BaseLogger):
    def __init__(self):
        """
        Initializes the TradeTopMostVisitedService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.trade_top_most_visited_dao = TradeTopMostVisitedDao(session)

    def save_trade_top_most_visited(self, data):
        """
        Saves a new trade top most visited entry.

        Parameters:
        - data (dict): Dictionary containing trade top most visited data.

        Returns:
        - int: Saved trade top most visited entry's ID
        """
        return self.trade_top_most_visited_dao.save_trade_top_most_visited(data)

    def get_all_trade_top_most_visited_entries(self):
        """
        Retrieves all trade top most visited entries.

        Returns:
        - list: List of all trade top most visited entries.
        """
        return self.trade_top_most_visited_dao.get_all_trade_top_most_visited_entries()

    def get_trade_top_most_visited_by_insCode(self, entry_id):
        """
        Retrieves a trade top most visited entry by its ID.

        Parameters:
        - entry_id (int): Trade top most visited entry ID to retrieve.

        Returns:
        - TradeTopMostVisited or None: Retrieved trade top most visited entry or None if not found.
        """
        return self.trade_top_most_visited_dao.get_trade_top_most_visited_by_insCode(entry_id)

    def get_trade_top_most_visited_by_market_name(self, marketName):
        """
        Retrieves a trade top most visited entry by its market name.

        Parameters:
        - entry_id (int): Trade top most visited entry ID to retrieve.

        Returns:
        - TradeTopMostVisited or None: Retrieved trade top most visited entry or None if not found.
        """
        return self.trade_top_most_visited_dao.get_trade_top_most_visited_by_marketName(marketName)

    def update_trade_top_most_visited(self, data):
        """
        Updates a trade top most visited entry.

        Parameters:
        - entry_id (int): Trade top most visited entry ID to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - int: Updated trade top most visited entry's ID
        """
        return self.trade_top_most_visited_dao.update_trade_top_most_visited(data)

    def delete_trade_top_most_visited_by_insCode(self, entry_id):
        """
        Deletes a trade top most visited entry by its ID.

        Parameters:
        - entry_id (int): Trade top most visited entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.trade_top_most_visited_dao.delete_trade_top_most_visited_by_insCode(entry_id)

    def create_table(self):
        """
        Create the trade_top_most_visited table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.trade_top_most_visited_dao.create_table()

    def get_insCodes_by_marketName(self, marketName):
        """
        Retrieves all insCodes by marketName.

        Returns:
        - list: List of all insCodes.
        """
        return self.trade_top_most_visited_dao.get_insCodes_by_marketName(marketName)

    def table_exists(self):
        """
        Create the insCodes table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.trade_top_most_visited_dao.table_exists()
