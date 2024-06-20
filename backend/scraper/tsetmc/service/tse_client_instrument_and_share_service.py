from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.instrument_info_dao import InstrumentInfoDao
from backend.scraper.tsetmc.dao.tse_client_instrument_and_share_dao import TseClientInstrumentAndShareDao
from backend.scraper.tsetmc.model.tse_client_instrument_info import TseClientInstrumentInfo

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class TseClientInstrumentAndShareService(BaseLogger):
    def __init__(self):
        """
        Initializes the TseClientInstrumentAndShareService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.tse_client_instrument_and_share_dao = TseClientInstrumentAndShareDao(session)

    def save_tse_client_instrument_info(self, data):
        """
        Saves a new instrument info entry.

        Parameters:
        - data (dict): Dictionary containing instrument info data.

        Returns:
        - int: Saved instrument info entry's ID
        """
        return self.tse_client_instrument_and_share_dao.save_instrument_info(data)

    def get_instrument_info_by_id(self, insCode):
        """
        Retrieves an instrument info entry by its ID.

        Parameters:
        - insCode (str): Instrument info entry ID to retrieve.

        Returns:
        - InstrumentInfo or None: Retrieved instrument info entry or None if not found.
        """
        return self.tse_client_instrument_and_share_dao.get_instrument_info_by_id(insCode)

    def add_or_update_instrument_info(self, items):
        updated_items = []
        for instrument_info in items:
            updated_item = self.tse_client_instrument_and_share_dao.add_or_update_instrument_info(instrument_info)
            updated_items.append(updated_item)
        return updated_items

    def add_or_update_share_info(self, items):
        updated_items = []
        for instrument_info in items:
            updated_item = self.tse_client_instrument_and_share_dao.add_or_update_share_info(instrument_info)
            updated_items.append(updated_item)
        return updated_items

    def add_or_update_closing_price_adjusted(self, items):
        updated_items = []
        for item in items:
            updated_item = self.tse_client_instrument_and_share_dao.add_or_update_closing_price_adjusted(item)
            updated_items.append(updated_item)
        return updated_items

    def update_instrument_info(self, data):
        """
        Updates an instrument info entry.

        Parameters:
        - insCode (str): Instrument info entry ID to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated instrument info entry's ID
        """
        updated_items = []
        for item in data:
            updated_item = self.tse_client_instrument_and_share_dao.update_instrument_info(item)
            updated_items.append(updated_item)

        return updated_items

    def delete_instrument_info_by_id(self, insCode):
        """
        Deletes an instrument info entry by its ID.

        Parameters:
        - insCode (str): Instrument info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.tse_client_instrument_and_share_dao.delete_instrument_info_by_id(insCode)

    def create_table_instrument_info(self):
        """
        Create the instrument_info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.tse_client_instrument_and_share_dao.create_table_instrument_info()

    def create_table_share_info(self):
        """
        Create the instrument_info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.tse_client_instrument_and_share_dao.create_table_share_info()

    def create_tables(self):
        """
        Create the
        tseClientinstrument_info
        tseClientshare_info
        tseClientclosingPriceAdjusted
        tables in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        t1 = self.tse_client_instrument_and_share_dao.create_table_share_info()
        t2 = self.tse_client_instrument_and_share_dao.create_table_instrument_info()
        t3 = self.tse_client_instrument_and_share_dao.create_table_closing_price_info_adjusted()
        return t1 and t2 and t3

    def get_all_ins_codes(self):
        """
        Retrieves all persian symbols.

        Returns:
        - list: List of all persian symbols.
        """
        return self.tse_client_instrument_and_share_dao.get_all_ins_codes()

    def table_exists(self):
        """
        Create the instrument_info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.tse_client_instrument_and_share_dao.table_exists()
