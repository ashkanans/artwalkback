from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.closing_price_daily_list_dao import ClosingPriceDailyListDao


class ClosingPriceDailyListService(BaseLogger):
    def __init__(self, dynamic_tablename):
        """
        Initializes the ClosingPriceDailyListService.

        Parameters:
        - dynamic_tablename: Dynamic table name for GetClosingPriceDailyList
        """
        # Creating the SQLAlchemy engine
        self.engine = create_engine(SQL_SERVER_URL)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.closing_price_dao = ClosingPriceDailyListDao(self.session, self.engine, dynamic_tablename)

    def save_closing_price_daily_list(self, data):
        """
        Saves a new closing price daily list entry.

        Parameters:
        - data (dict): Dictionary containing closing price daily list data.

        Returns:
        - datetime: Saved closing price daily list entry's datetime
        """
        return self.closing_price_dao.save_closing_price_daily_list(data)

    def get_all_closing_price_daily_list_entries(self):
        """
        Retrieves all closing price daily list entries.

        Returns:
        - list: List of all closing price daily list entries.
        """
        return self.closing_price_dao.get_all_closing_price_daily_list_entries()

    def get_closing_price_daily_list_by_datetime(self, datetime):
        """
        Retrieves a closing price daily list entry by its datetime.

        Parameters:
        - datetime: Datetime of the closing price daily list entry to retrieve.

        Returns:
        - GetClosingPriceDailyList or None: Retrieved closing price daily list entry or None if not found.
        """
        return self.closing_price_dao.get_closing_price_daily_list_by_datetime(datetime)

    def update_closing_price_daily_list(self, data):
        """
        Updates a closing price daily list entry.

        Parameters:
        - datetime: Datetime of the closing price daily list entry to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - datetime: Updated closing price daily list entry's datetime
        """
        return self.closing_price_dao.update_closing_price_daily_list(data)

    def delete_closing_price_daily_list_by_datetime(self, datetime):
        """
        Deletes a closing price daily list entry by its datetime.

        Parameters:
        - datetime: Datetime of the closing price daily list entry to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.closing_price_dao.delete_closing_price_daily_list_by_datetime(datetime)

    def create_table(self):
        """
        Create the closing_price_daily_list table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.closing_price_dao.create_table()

    def table_exists(self):
        """
        Create the closing_price_daily_list table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.closing_price_dao.table_exists()

    def get_closing_price_daily_list_last_30_items(self):
        """
        Retrieves a closing price daily list entry last 30 items based on datetime_str.

        Returns:
        - GetClosingPriceDailyList or None: Retrieved closing price daily list entry or None if not found.
        """
        return self.closing_price_dao.get_closing_price_daily_list_last_30_items()
