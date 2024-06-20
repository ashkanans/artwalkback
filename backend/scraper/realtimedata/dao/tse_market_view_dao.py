from sqlalchemy import inspect
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.realtimedata.model.tse_market_view import TseMarketView  # Update import


class TseMarketViewDao(BaseLogger):  # Update class name
    def __init__(self, session: Session, engine):
        super().__init__()
        """
        Initializes the TseMarketViewDao.

        Parameters:
        - session: SQLAlchemy session object
        - engine: SQLAlchemy engine object
        """
        self.session = session
        self.engine = engine

    def save_tse_market_view_entry(self, data):  # Update method name
        """
        Saves a new TseMarketView entry.

        Parameters:
        - data (dict): Dictionary containing TseMarketView data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        try:
            tse_market_view_entry = TseMarketView(data)  # Update model object
            self.session.add(tse_market_view_entry)
            self.session.commit()
            self.logger.info(f"Saved TseMarketView row: {data}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving TseMarketView entry: {e}")
            self.session.rollback()
            return False

    def get_all_tse_market_view_entries(self):  # Update method name
        """
        Retrieves all TseMarketView entries.

        Returns:
        - list: List of all TseMarketView entries.
        """
        return self.session.query(TseMarketView).all()  # Update model object

    def update_tse_market_view_entry(self, data):  # Update method name
        """
        Updates a TseMarketView entry.

        Parameters:
        - entry_id: ID of the TseMarketView entry to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        try:
            self.save_tse_market_view_entry(data)  # Update method call
        except Exception as e:
            self.logger.error(f"Error updating TseMarketView entry: {e}")
            self.session.rollback()
            return False

    def delete_all_tse_market_view_entries(self):  # Update method name
        """
        Deletes all entries from the TseMarketView table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        try:
            self.session.execute(TseMarketView.__table__.delete())  # Update model object

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error deleting all TseMarketView entries: {e}")
            self.session.rollback()
            return False

    def table_exists(self):
        """
        Check if the TseMarketView table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.engine)
        return inspector.has_table(TseMarketView.__tablename__)

    def create_table(self):
        """
        Create the desired table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                TseMarketView.__table__.create(self.session.bind)  # Update model object
                self.logger.info(f"Table created: {TseMarketView.__tablename__}")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info(f"Table {TseMarketView.__tablename__} already exists. ")
        return False


