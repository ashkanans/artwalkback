from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.instrument_info_dao import InstrumentInfoDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class InstrumentInfoService(BaseLogger):
    def __init__(self):
        """
        Initializes the InstrumentInfoService.

        Parameters:
        - session: SQLAlchemy session object
        """
        super().__init__()
        self.instrument_info_dao = InstrumentInfoDao(session)

    def save_instrument_info(self, data):
        """
        Saves a new instrument info entry.

        Parameters:
        - data (dict): Dictionary containing instrument info data.

        Returns:
        - int: Saved instrument info entry's ID
        """
        return self.instrument_info_dao.save_instrument_info(data)

    def get_all_instrument_info_entries(self):
        """
        Retrieves all instrument info entries.

        Returns:
        - list: List of all instrument info entries.
        """
        return self.instrument_info_dao.get_all_instrument_info_entries()

    def get_instrument_info_by_id(self, insCode):
        """
        Retrieves an instrument info entry by its ID.

        Parameters:
        - insCode (str): Instrument info entry ID to retrieve.

        Returns:
        - InstrumentInfo or None: Retrieved instrument info entry or None if not found.
        """
        return self.instrument_info_dao.get_instrument_info_by_id(insCode)

    def get_instrument_info_by_persian_symbol(self, symbolFa):
        """
        Retrieves an instrument info entry by its persian symbol.

        Parameters:
        - symbolFa (str): Instrument info entry persian symbol to retrieve.

        Returns:
        - InstrumentInfo or None: Retrieved instrument info entry or None if not found.
        """
        return self.instrument_info_dao.get_instrument_info_by_persian_symbol(symbolFa)

    def update_instrument_info(self, data):
        """
        Updates an instrument info entry.

        Parameters:
        - insCode (str): Instrument info entry ID to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated instrument info entry's ID
        """
        eps = data.get("eps")
        if eps:
            data["epsValue"] = eps.get("epsValue")
            data["estimatedEPS"] = eps.get("estimatedEPS")
            data["sectorPE"] = eps.get("sectorPE")
            data["psr"] = eps.get("psr")
            data.pop("eps")

        sector = data.get("sector")
        if sector:
            data["cSecVal"] = sector.get("cSecVal")
            data["lSecVal"] = sector.get("lSecVal")
            data.pop("sector")

        staticTreshhold = data.get("staticThreshold")
        if staticTreshhold:
            data["psGelStaMax"] = staticTreshhold.get("psGelStaMax")
            data["psGelStaMin"] = staticTreshhold.get("psGelStaMin")
            data.pop("staticThreshold")

        return self.instrument_info_dao.update_instrument_info(data)

    def delete_instrument_info_by_id(self, insCode):
        """
        Deletes an instrument info entry by its ID.

        Parameters:
        - insCode (str): Instrument info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.instrument_info_dao.delete_instrument_info_by_id(insCode)

    def create_table(self):
        """
        Create the instrument_info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.instrument_info_dao.create_table()

    def get_insCodes_englishName_persianName(self):
        """
        Retrieves all insCodes by marketName.

        Returns:
        - list: List of all insCodes.
        """
        return self.instrument_info_dao.get_insCodes_englishName_persianName()

    def get_all_persian_symbols(self):
        """
        Retrieves all persian symbols.

        Returns:
        - list: List of all persian symbols.
        """
        return self.instrument_info_dao.get_all_persian_symbols()

    def get_all_ins_codes(self):
        """
        Retrieves all persian symbols.

        Returns:
        - list: List of all persian symbols.
        """
        return self.instrument_info_dao.get_all_ins_codes()

    def table_exists(self):
        """
        Create the instrument_info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.instrument_info_dao.table_exists()

    def get_all_persian_symbols_by_sector_code(self, param):
        return self.instrument_info_dao.get_all_persian_symbols_by_sector_code(param)

    def get_list_data(self, inscode):
        return self.instrument_info_dao.get_list_data(inscode)
