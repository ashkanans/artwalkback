from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.realtimedata.dao.price_table_dao import PriceTableDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL.replace("cm", "realtime"))
Session = sessionmaker(bind=engine)
session = Session()


class PriceTableService:
    def __init__(self):
        """
        Initializes the PriceTableService.
        """
        self.price_table_dao = PriceTableDao(session)

    def save_price_table(self, data):
        """
        Saves a new price table entry.

        Parameters:
        - data (dict): Dictionary containing price table data.

        Returns:
        - PriceTable: Saved price table object.
        """
        return self.price_table_dao.save_price_table(data)

    def get_all_price_tables(self):
        """
        Retrieves all price tables.

        Returns:
        - list: List of all price tables.
        """
        return self.price_table_dao.get_all_price_tables()

    def get_price_table_by_currency_name(self, currency_name):
        """
        Retrieves a price table by its currency name.

        Parameters:
        - currency_name (str): Currency name to retrieve.

        Returns:
        - PriceTable or None: Retrieved price table or None if not found.
        """
        return self.price_table_dao.get_price_table_by_currency_name(currency_name)

    def update_price_table(self, data):
        """
        Updates a price table.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - PriceTable or None: Updated price table object or None if not found.
        """
        return self.price_table_dao.update_price_table(data)

    def delete_price_table(self, currency_name):
        """
        Deletes a price table by its currency name.

        Parameters:
        - currency_name (str): Currency name to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.price_table_dao.delete_price_table(currency_name)

    def create_table(self):
        """
        Create the price_table table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.price_table_dao.create_table()

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.price_table_dao.table_exists()
