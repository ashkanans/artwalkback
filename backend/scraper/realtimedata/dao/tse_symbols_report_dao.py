from sqlalchemy import inspect
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.realtimedata.model.tse_symbols_report import TseSymbolsReport  # Update import


class TseSymbolsReportDao(BaseLogger):  # Update class name
    def __init__(self, session: Session, engine):
        super().__init__()
        """
        Initializes the TseSymbolsReportDao.

        Parameters:
        - session: SQLAlchemy session object
        - engine: SQLAlchemy engine object
        """
        self.session = session
        self.engine = engine


    def save_tse_symbols_report_entry(self, data):  # Update method name
        """
        Saves a new TseSymbolsReport entry.

        Parameters:
        - data (dict): Dictionary containing TseSymbolsReport data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        try:
            tse_symbols_report_entry = TseSymbolsReport(data)  # Update model object
            self.session.add(tse_symbols_report_entry)
            self.session.commit()
            self.logger.info(f"Saved TseSymbolsReport row: {data}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving TseSymbolsReport entry: {e}")
            self.session.rollback()
            return False

    def get_all_tse_symbols_report_entries(self):  # Update method name
        """
        Retrieves all TseSymbolsReport entries.

        Returns:
        - list: List of all TseSymbolsReport entries.
        """
        return self.session.query(TseSymbolsReport).all()  # Update model object

    def update_tse_symbols_report_entry(self, data):  # Update method name
        """
        Updates a TseSymbolsReport entry.

        Parameters:
        - entry_id: ID of the TseSymbolsReport entry to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        try:
            self.save_tse_symbols_report_entry(data)  # Update method call
        except Exception as e:
            self.logger.error(f"Error updating TseSymbolsReport entry: {e}")
            self.session.rollback()
            return False

    def delete_all_tse_symbols_report_entries(self):  # Update method name
        """
        Deletes all entries from the TseSymbolsReport table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        try:
            self.session.execute(TseSymbolsReport.__table__.delete())  # Update model object

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error deleting all TseSymbolsReport entries: {e}")
            self.session.rollback()
            return False

    def table_exists(self):
        """
        Check if the TseSymbolsReport table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.engine)
        return inspector.has_table(TseSymbolsReport.__tablename__)

    def create_table(self):
        """
        Create the desired table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                TseSymbolsReport.__table__.create(self.session.bind)  # Update model object
                self.logger.info(f"Table created: {TseSymbolsReport.__tablename__}")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info(f"Table {TseSymbolsReport.__tablename__} already exists. ")
        return False


