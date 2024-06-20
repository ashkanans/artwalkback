from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.market_overview_dao import MarketOverviewDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class MarketOverviewService(BaseLogger):
    def __init__(self):
        """
        Initializes the MarketOverviewService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.market_overview_dao = MarketOverviewDao(session)

    def save_market_overview(self, data):
        """
        Saves a new market overview.

        Parameters:
        - data (dict): Dictionary containing market overview data.

        Returns:
        - MarketOverview: Saved market overview object.
        """
        return self.market_overview_dao.save_market_overview(data)

    def get_all_market_overviews(self):
        """
        Retrieves all market overviews.

        Returns:
        - list: List of all market overviews.
        """
        return self.market_overview_dao.get_all_market_overviews()

    def get_market_overview_by_id(self, market_overview_id):
        """
        Retrieves a market overview by its ID.

        Parameters:
        - market_overview_id (int): Market overview ID to retrieve.

        Returns:
        - MarketOverview or None: Retrieved market overview or None if not found.
        """
        return self.market_overview_dao.get_market_overview_by_name(market_overview_id)

    def update_market_overview(self, data, id):
        """
        Updates a market overview.

        Parameters:
        - market_overview_id (int): Market overview ID to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - MarketOverview or None: Updated market overview object or None if not found.
        """
        return self.market_overview_dao.update_market_overview(data, id)

    def delete_market_overview(self, market_overview_id):
        """
        Deletes a market overview by its ID.

        Parameters:
        - market_overview_id (int): Market overview ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.market_overview_dao.delete_market_overview(market_overview_id)

    def create_table(self):
        """
        Create the market_overview table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.market_overview_dao.create_table()

    def table_exists(self):
        """
        Create the market_overview table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.market_overview_dao.table_exists()
