from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.best_limits_dao import BestLimitsDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class BestLimitsService(BaseLogger):
    def __init__(self):
        """
        Initializes the BestLimitsService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.best_limits_dao = BestLimitsDao(session)

    def save_best_limits(self, data):
        """
        Saves a new best limits  entry.

        Parameters:
        - data (dict): Dictionary containing best limits  data.

        Returns:
        - int: Saved best limits  entry's key
        """
        return self.best_limits_dao.save_best_limits(data)

    def get_all_best_limits_entries(self):
        """
        Retrieves all best limits  entries.

        Returns:
        - list: List of all best limits  entries.
        """
        return self.best_limits_dao.get_all_best_limits_entries()

    def get_best_limits_by_key(self, code):
        """
        Retrieves a best limits  entry by its key.

        Parameters:
        - code (str): best limits  entry key to retrieve.

        Returns:
        - BestLimits or None: Retrieved best limits  entry or None if not found.
        """
        return self.best_limits_dao.get_best_limits_by_key(code)

    def update_best_limits(self, data):
        """
        Updates a best limits  entry.

        Parameters:
        - code (str): best limits  entry key to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated best limits  entry's key
        """

        return self.best_limits_dao.update_best_limits(data)

    def delete_best_limits_by_key(self, code):
        """
        Deletes a best limits  entry by its key.

        Parameters:
        - code (str): best limits  entry key to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.best_limits_dao.delete_best_limits_by_key(code)

    def create_table(self):
        """
        Create the best limits table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.best_limits_dao.create_table()

    def table_exists(self):
        """
        Create the best limits table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """

        return self.best_limits_dao.table_exists()

    def get_row_data(self, inscode, number):
        return BestLimitsDao.get_row_data(self, inscode, number)

    def get_list_data(self, inscode):
        return BestLimitsDao.get_list_data(self, inscode)
