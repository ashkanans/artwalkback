from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.realtimedata.dao.tse_industry_indexes_dao import TseIndustryIndexesDao  # Update import

engine = create_engine(SQL_SERVER_URL.replace("cm", "realtime"))
Session = sessionmaker(bind=engine)
session = Session()


class TseIndustryIndexesService:  # Update class name
    def __init__(self):
        """
        Initializes the TseIndustryIndexes.

        Parameters:
        - dynamic_tablename: Dynamic table name for TseIndustryIndexes
        """
        # Creating the SQLAlchemy engine

        self.tse_industry_indexes_dao = TseIndustryIndexesDao(session, engine)  # Update dao object

    def save_tse_industry_indexes_entry(self, data):  # Update method name
        """
        Saves a new TseIndustryIndexes entry.

        Parameters:
        - data (dict): Dictionary containing TseIndustryIndexes data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        return self.tse_industry_indexes_dao.save_tse_industry_indexes_entry(data)  # Update method call

    def get_all_tse_industry_indexes_entries(self):  # Update method name
        """
        Retrieves all TseIndustryIndexes entries.

        Returns:
        - list: List of all TseIndustryIndexes entries.
        """
        return self.tse_industry_indexes_dao.get_all_tse_industry_indexes_entries()  # Update method call

    def update_tse_industry_indexes_entry(self, data):  # Update method name
        """
        Updates a TseIndustryIndexes entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        return self.tse_industry_indexes_dao.update_tse_industry_indexes_entry(data)  # Update method call

    def delete_all_tse_industry_indexes_entries(self):  # Update method name
        """
        Deletes all entries from the TseIndustryIndexes table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.tse_industry_indexes_dao.delete_all_tse_industry_indexes_entries()  # Update method call

    def table_exists(self):
        """
        Check if the TseIndustryIndexes table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.tse_industry_indexes_dao.table_exists()  # Update method call

    def create_table(self):
        """
        Create the desired table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.tse_industry_indexes_dao.create_table()  # Update method call
