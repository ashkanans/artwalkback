import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.tradingeconomics.dao.categories_dao import CategoriesDao
from backend.scraper.logger.base_logger import BaseLogger

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class CategoriesService(BaseLogger):
    def __init__(self):
        """
        Initializes the CategoriesService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.categories_dao = CategoriesDao(session)

    def save_Categories(self, data):
        """
        Saves a new categories.

        Parameters:
        - data (dict): Dictionary containing categories data.

        Returns:
        - Categories: Saved categories object.
        """
        return self.categories_dao.save_categories(data)

    def get_all_Categories(self):
        """
        Retrieves all categories.

        Returns:
        - list: List of all categories.
        """
        return self.categories_dao.get_all_categoriess()
    
    def get_all_urls(self):
        """
        Retrieves all categories urls.

        Returns:
        - list: List of all categories urls.
        """
        return self.categories_dao.get_all_urls()

    def update_Categories(self, data):
        """
        Updates a categories.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - Categories or None: Updated categories object or None if not found.
        """
        return self.categories_dao.update_categories(data)

    def delete_Categories(self, name):
        """
        Deletes a categories by its tracing number.

        Parameters:
        - tracing_no (int): Tracing number to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.categories_dao.delete_categories(name)

    def create_table(self):
        """
        Create the categories table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.categories_dao.create_table()

    def extract_date(self, input_string):
        # Use regular expression to find the date pattern
        match = re.search(r'\b(\d{4}/\d{2}/\d{2})\b', input_string)

        if match:
            # Extract the matched date and return it
            return match.group(1)
        else:
            # Return None if no date is found in the input string
            return None

    def table_exists(self):
        """
        Create the instrument_info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.categories_dao.table_exists()
