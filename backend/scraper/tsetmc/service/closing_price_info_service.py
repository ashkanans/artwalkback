from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.closing_price_info_dao import ClosingPriceInfoDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class ClosingPriceInfoService(BaseLogger):
    def __init__(self):
        """
        Initializes the ClosingPriceInfoService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.closing_price_info_dao = ClosingPriceInfoDao(session)

    def save_closing_price_info(self, data):
        """
        Saves a new closing price info  entry.

        Parameters:
        - data (dict): Dictionary containing closing price info  data.

        Returns:
        - int: Saved closing price info  entry's inscode
        """
        return self.closing_price_info_dao.save_closing_price_info(data)

    def get_all_closing_price_info_entries(self):
        """
        Retrieves all closing price info  entries.

        Returns:
        - list: List of all closing price info  entries.
        """
        return self.closing_price_info_dao.get_all_closing_price_info_entries()

    def get_closing_price_info_by_inscode(self, code):
        """
        Retrieves a closing price info  entry by its inscode.

        Parameters:
        - code (str): closing price info  entry inscode to retrieve.

        Returns:
        - ClosingPriceInfo or None: Retrieved closing price info  entry or None if not found.
        """
        return self.closing_price_info_dao.get_closing_price_info_by_inscode(code)

    def update_closing_price_info(self, data):
        """
        Updates a closing price info  entry.

        Parameters:
        - code (str): closing price info  entry inscode to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated closing price info  entry's inscode
        """

        return self.closing_price_info_dao.update_closing_price_info(data)

    def delete_closing_price_info_by_inscode(self, code):
        """
        Deletes a closing price info  entry by its inscode.

        Parameters:
        - code (str): closing price info  entry inscode to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.closing_price_info_dao.delete_closing_price_info_by_inscode(code)

    def create_table(self):
        """
        Create the closing price info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.closing_price_info_dao.create_table()

    def table_exists(self):
        """
        Create the closing price info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """

        return self.closing_price_info_dao.table_exists()

    def get_list_data(self, inscode):
        return ClosingPriceInfoDao.get_list_data(self, inscode)
