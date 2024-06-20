from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.realtimedata.dao.tse_market_view_dao import TseMarketViewDao  # Update import

engine = create_engine(SQL_SERVER_URL.replace("cm", "realtime"))
Session = sessionmaker(bind=engine)
session = Session()


class TseMarketViewService:  # Update class name
    def __init__(self):
        """
        Initializes the TseMarketViewService.

        Parameters:
        - dynamic_tablename: Dynamic table name for TseMarketView
        """
        # Creating the SQLAlchemy engine

        self.tse_market_view_dao = TseMarketViewDao(session, engine)  # Update dao object

    def save_tse_market_view_entry(self, data):  # Update method name
        """
        Saves a new TseMarketView entry.

        Parameters:
        - data (dict): Dictionary containing TseMarketView data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        return self.tse_market_view_dao.save_tse_market_view_entry(data)  # Update method call

    def get_all_tse_market_view_entries(self):  # Update method name
        """
        Retrieves all TseMarketView entries.

        Returns:
        - list: List of all TseMarketView entries.
        """
        return self.tse_market_view_dao.get_all_tse_market_view_entries()  # Update method call

    def update_tse_market_view_entry(self, data):  # Update method name
        """
        Updates a TseMarketView entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        return self.tse_market_view_dao.update_tse_market_view_entry(data)  # Update method call

    def delete_all_tse_market_view_entries(self):  # Update method name
        """
        Deletes all entries from the TseMarketView table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.tse_market_view_dao.delete_all_tse_market_view_entries()  # Update method call

    def table_exists(self):
        """
        Check if the TseMarketView table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.tse_market_view_dao.table_exists()  # Update method call

    def create_table(self):
        """
        Create the desired table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.tse_market_view_dao.create_table()  # Update method call


