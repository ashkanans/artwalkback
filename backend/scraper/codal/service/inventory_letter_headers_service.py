from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.codal.dao.inventory_letter_headers_dao import InventoryLetterHeadersDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class InventoryLetterHeadersService:
    def __init__(self):
        """
        Initializes the service for CodalInventoryLetterHeaders.
        """
        self.inventory_letter_headers_dao = InventoryLetterHeadersDao(session)

    def save_entry(self, data):
        """
        Saves a new entry.

        Parameters:
        - data (dict): Dictionary containing entry data.

        Returns:
        - Entry: Saved entry object.
        """
        return self.inventory_letter_headers_dao.save_entry(data)

    def get_all_entries(self):
        """
        Retrieves all entries.

        Returns:
        - list: List of all entries.
        """
        return self.inventory_letter_headers_dao.get_all_entries()

    def get_entry_by_id(self, entry_id):
        """
        Retrieves an entry by its ID.

        Parameters:
        - entry_id (int): ID of the entry to retrieve.

        Returns:
        - Entry or None: Retrieved entry or None if not found.
        """
        return self.inventory_letter_headers_dao.get_entry_by_id(entry_id)

    def update_entry(self, data):
        """
        Updates an entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - Entry or None: Updated entry object or None if not found.
        """
        return self.inventory_letter_headers_dao.update_entry(data)

    def delete_entry_by_id(self, entry_id):
        """
        Deletes an entry by its ID.

        Parameters:
        - entry_id (int): ID of the entry to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.inventory_letter_headers_dao.delete_entry_by_id(entry_id)

    def create_table(self):
        """
        Creates the table for CodalInventoryLetterHeaders in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.inventory_letter_headers_dao.create_table()

    def table_exists(self):
        """
        Checks if the table for CodalInventoryLetterHeaders exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.inventory_letter_headers_dao.table_exists()

    def get_all_symbol_headers_by_type(self, symbol, type):
        return self.inventory_letter_headers_dao.get_all_symbol_headers_by_type(symbol,type)