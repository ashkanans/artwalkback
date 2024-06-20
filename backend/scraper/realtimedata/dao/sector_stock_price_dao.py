from sqlalchemy import inspect
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.realtimedata.model.sector_stock_price import SectorStockPrice


class SectorStockPriceDao(BaseLogger):
    def __init__(self, session: Session, engine, dynamic_tablename: str):
        super().__init__()
        """
        Initializes the SectorStockPriceDao.

        Parameters:
        - session: SQLAlchemy session object
        - engine: SQLAlchemy engine object
        - dynamic_tablename: Dynamic table name for SectorStockPrice
        """
        self.session = session
        self.engine = engine
        self.dynamic_tablename = dynamic_tablename

        # Set the dynamic table name for SectorStockPrice
        SectorStockPrice.__table__.name = dynamic_tablename

    def save_sector_stock_price_entry(self, data):
        """
        Saves a new SectorStockPrice entry.

        Parameters:
        - data (dict): Dictionary containing SectorStockPrice data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        try:
            sector_stock_price_entry = SectorStockPrice(data)
            self.session.add(sector_stock_price_entry)
            self.session.commit()
            self.logger.info(f"Saved SectorStockPrice entry: {data}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving SectorStockPrice entry: {e}")
            self.session.rollback()
            return False

    def get_all_sector_stock_price_entries(self):
        """
        Retrieves all SectorStockPrice entries.

        Returns:
        - list: List of all SectorStockPrice entries.
        """
        return self.session.query(SectorStockPrice).all()

    def delete_all_sector_stock_price_entries(self):
        """
        Deletes all entries from the SectorStockPrice table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        try:
            self.session.execute(SectorStockPrice.__table__.delete())

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error deleting all SectorStockPrice entries: {e}")
            self.session.rollback()
            return False

    def table_exists(self):
        """
        Check if the SectorStockPrice table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.engine)
        return inspector.has_table(self.dynamic_tablename)

    def create_table(self):
        """
        Create the desired table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                SectorStockPrice.__table__.create(self.session.bind)
                self.logger.info(f"Table created: {self.dynamic_tablename}")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info(f"Table {self.dynamic_tablename} already exists. ")
        return False

    def update_sector_stock_price(self, data):
        """
        Updates a SectorStockPrice entry.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        try:
            self.save_sector_stock_price_entry(data)
        except Exception as e:
            self.logger.error(f"Error updating MonthlyPerformance entry: {e}")
            self.session.rollback()
            return False
