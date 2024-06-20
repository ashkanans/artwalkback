from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.realtimedata.dao.sector_stock_price_dao import SectorStockPriceDao


class SectorStockPriceService:
    def __init__(self, dynamic_tablename):
        """
        Initializes the SectorStockPriceService.

        Parameters:
        - dynamic_tablename: Dynamic table name for SectorStockPrice
        """
        # Creating the SQLAlchemy engine
        self.engine = create_engine(SQL_SERVER_URL.replace("cm", "realtime"))
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.sector_stock_price_dao = SectorStockPriceDao(self.session, self.engine, dynamic_tablename)

    def save_sector_stock_price_entry(self, data):
        """
        Saves a new SectorStockPrice entry.

        Parameters:
        - data (dict): Dictionary containing SectorStockPrice data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        return self.sector_stock_price_dao.save_sector_stock_price_entry(data)

    def get_all_sector_stock_price_entries(self):
        """
        Retrieves all SectorStockPrice entries.

        Returns:
        - list: List of all SectorStockPrice entries.
        """
        return self.sector_stock_price_dao.get_all_sector_stock_price_entries()

    def delete_all_sector_stock_price_entries(self):
        """
        Deletes all entries from the SectorStockPrice table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.sector_stock_price_dao.delete_all_sector_stock_price_entries()

    def create_table(self):
        """
        Create the sector_stock_price table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.sector_stock_price_dao.create_table()

    def table_exists(self):
        """
        Check if the sector_stock_price table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.sector_stock_price_dao.table_exists()

    def update_sector_stock_price(self, data):
        """
        Updates a SectorStockPrice entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        return self.sector_stock_price_dao.update_sector_stock_price(data)  # Update method call
