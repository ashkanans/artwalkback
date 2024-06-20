from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.instrument_shareholder_last_dao import InstrumentShareholderLastDao


class InstrumentShareholderLastService(BaseLogger):
    def __init__(self, dynamic_tablename):
        """
        Initializes the InstrumentShareholderLastService.

        Parameters:
        - dynamic_tablename: Dynamic table name for GetInstrumentShareholderLast
        """
        # Creating the SQLAlchemy engine
        self.engine = create_engine(SQL_SERVER_URL)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.instrument_shareholder_dao = InstrumentShareholderLastDao(self.session, self.engine, dynamic_tablename)

    def save_instrument_shareholder_last(self, data):
        """
        Saves a new instrument shareholder last entry.

        Parameters:
        - data (dict): Dictionary containing instrument shareholder last data.

        Returns:
        - datetime: Saved instrument shareholder last entry's datetime
        """
        return self.instrument_shareholder_dao.save_instrument_shareholder_last(data)

    def get_all_instrument_shareholder_last_entries(self):
        """
        Retrieves all instrument shareholder last entries.

        Returns:
        - list: List of all instrument shareholder last entries.
        """
        return self.instrument_shareholder_dao.get_all_instrument_shareholder_last_entries()

    def get_instrument_shareholder_last_by_datetime(self, datetime):
        """
        Retrieves an instrument shareholder last entry by its datetime.

        Parameters:
        - datetime: Datetime of the instrument shareholder last entry to retrieve.

        Returns:
        - GetInstrumentShareholderLast or None: Retrieved instrument shareholder last entry or None if not found.
        """
        return self.instrument_shareholder_dao.get_instrument_shareholder_last_by_datetime(datetime)

    def update_instrument_shareholder_last(self, data):
        """
        Updates an instrument shareholder last entry.

        Parameters:
        - datetime: Datetime of the instrument shareholder last entry to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - datetime: Updated instrument shareholder last entry's datetime
        """
        return self.instrument_shareholder_dao.update_instrument_shareholder_last(data)

    def delete_instrument_shareholder_last_by_datetime(self, datetime):
        """
        Deletes an instrument shareholder last entry by its datetime.

        Parameters:
        - datetime: Datetime of the instrument shareholder last entry to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.instrument_shareholder_dao.delete_instrument_shareholder_last_by_datetime(datetime)

    def create_table(self):
        """
        Create the instrument_shareholder_last table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.instrument_shareholder_dao.create_table()

    def table_exists(self):
        """
        Check if the instrument_shareholder_last table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.instrument_shareholder_dao.table_exists()

    def get_instrument_shareholder_last_last_30_items(self):
        """
        Retrieves an instrument shareholder last entry last 30 items based on datetime_str.

        Returns:
        - GetInstrumentShareholderLast or None: Retrieved instrument shareholder last entry or None if not found.
        """
        return self.instrument_shareholder_dao.get_instrument_shareholder_last_last_30_items()
