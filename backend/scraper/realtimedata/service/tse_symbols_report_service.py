from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.realtimedata.dao.tse_symbols_report_dao import TseSymbolsReportDao  # Update import

engine = create_engine(SQL_SERVER_URL.replace("cm", "realtime"))
Session = sessionmaker(bind=engine)
session = Session()


class TseSymbolsReportService:  # Update class name
    def __init__(self):
        """
        Initializes the TseSymbolsReportService.

        Parameters:
        - dynamic_tablename: Dynamic table name for TseSymbolsReport
        """
        # Creating the SQLAlchemy engine

        self.tse_symbols_report_dao = TseSymbolsReportDao(session, engine)  # Update dao object

    def save_tse_symbols_report_entry(self, data):  # Update method name
        """
        Saves a new TseSymbolsReport entry.

        Parameters:
        - data (dict): Dictionary containing TseSymbolsReport data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        return self.tse_symbols_report_dao.save_tse_symbols_report_entry(data)  # Update method call

    def get_all_tse_symbols_report_entries(self):  # Update method name
        """
        Retrieves all TseSymbolsReport entries.

        Returns:
        - list: List of all TseSymbolsReport entries.
        """
        return self.tse_symbols_report_dao.get_all_tse_symbols_report_entries()  # Update method call

    def update_tse_symbols_report_entry(self, data):  # Update method name
        """
        Updates a TseSymbolsReport entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        return self.tse_symbols_report_dao.update_tse_symbols_report_entry(data)  # Update method call

    def delete_all_tse_symbols_report_entries(self):  # Update method name
        """
        Deletes all entries from the TseSymbolsReport table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.tse_symbols_report_dao.delete_all_tse_symbols_report_entries()  # Update method call

    def table_exists(self):
        """
        Check if the TseSymbolsReport table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.tse_symbols_report_dao.table_exists()  # Update method call

    def create_table(self):
        """
        Create the desired table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.tse_symbols_report_dao.create_table()  # Update method call

