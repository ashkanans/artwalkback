from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.realtimedata.dao.inventory_letter_dao import InventoryLetterDao  # Update import


class InventoryLetterService:  # Update class name
    def __init__(self, dynamic_tablename):
        """
        Initializes the InventoryLetterService.

        Parameters:
        - dynamic_tablename: Dynamic table name for InventoryLetter
        """
        # Creating the SQLAlchemy engine
        self.engine = create_engine(SQL_SERVER_URL.replace("cm", "realtime"))
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.inventory_letter_dao = InventoryLetterDao(self.session, self.engine,
                                                             dynamic_tablename)  # Update dao object

    def save_inventory_letter_entry(self, data):  # Update method name
        """
        Saves a new InventoryLetter entry.

        Parameters:
        - data (dict): Dictionary containing InventoryLetter data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        return self.inventory_letter_dao.save_inventory_letter_entry(data)  # Update method call

    def get_all_inventory_letter_entries(self):  # Update method name
        """
        Retrieves all InventoryLetter entries.

        Returns:
        - list: List of all InventoryLetter entries.
        """
        return self.inventory_letter_dao.get_all_inventory_letter_entries()  # Update method call

    def update_inventory_letter_entry(self, data):  # Update method name
        """
        Updates a InventoryLetter entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        return self.inventory_letter_dao.update_inventory_letter_entry(data)  # Update method call

    def delete_all_inventory_letter_entries(self):  # Update method name
        """
        Deletes all entries from the InventoryLetter table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.inventory_letter_dao.delete_all_inventory_letter_entries()  # Update method call

    def table_exists(self):
        """
        Check if the InventoryLetter table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.inventory_letter_dao.table_exists()  # Update method call

    def create_table(self):
        """
        Create the desired table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.inventory_letter_dao.create_table()  # Update method call

