from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.closing_price_info_adjusted import ClosingPriceInfoAdjusted
from backend.scraper.tsetmc.model.tse_client_instrument_info import TseClientInstrumentInfo
from backend.scraper.tsetmc.model.tse_client_share_info import TseClientShareInfo

Base = declarative_base()


class TseClientInstrumentAndShareDao(BaseLogger):
    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the TseClientInstrumentAndShareDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_instrument_info(self, data):
        """
        Saves a new instrument info entry.

        Parameters:
        - data (dict): Dictionary containing instrument info data.

        Returns:
        - int: Saved instrument info entry's ID
        """
        instrument_info = TseClientInstrumentInfo(**data)
        self.session.add(instrument_info)
        self.session.commit()
        self.logger.info(f"Saved tse client instrument info entry with ID: {instrument_info.insCode}")
        return instrument_info.insCode

    def get_all_instrument_info_entries(self):
        """
        Retrieves all instrument info entries.

        Returns:
        - list: List of all instrument info entries.
        """
        return self.session.query(TseClientInstrumentInfo).all()

    def add_or_update_instrument_info(self, item):
        existing_instrument = self.session.query(TseClientInstrumentInfo).filter_by(insCode=item.insCode).first()
        if existing_instrument:
            # Update existing record
            for key, value in item.__dict__.items():
                setattr(existing_instrument, key, value)
        else:
            # Add new record
            self.session.add(item)
        self.session.commit()

    def add_or_update_share_info(self, item):
        existing_instrument = self.session.query(TseClientShareInfo).filter_by(insCode=item.insCode).first()
        if existing_instrument:
            # Update existing record
            for key, value in item.__dict__.items():
                setattr(existing_instrument, key, value)
        else:
            # Add new record
            self.session.add(item)
        self.session.commit()

    def get_instrument_info_by_id(self, insCode):
        """
        Retrieves an instrument info entry by its ID.

        Parameters:
        - insCode (str): Instrument info entry ID to retrieve.

        Returns:
        - InstrumentInfo or None: Retrieved instrument info entry or None if not found.
        """
        return self.session.query(TseClientInstrumentInfo).filter_by(insCode=insCode).first()

    def update_instrument_info(self, data):
        """
        Updates an instrument info entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated instrument info entry's ID
        """
        try:
            existing_record = self.get_instrument_info_by_id(data.insCode)

            for key, value in data.items():
                setattr(existing_record, key, value)

            self.session.commit()
            self.logger.info(f"Updated instrument info entry with ID: {existing_record.insCode}")
            return existing_record.insCode

        except NoResultFound:
            return self.save_instrument_info(data)

    def delete_instrument_info_by_id(self, insCode):
        """
        Deletes an instrument info entry by its ID.

        Parameters:
        - insCode (str): Instrument info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        instrument_info = self.session.query(TseClientInstrumentInfo).filter_by(insCode=insCode).first()
        if instrument_info:
            self.session.delete(instrument_info)
            self.session.commit()
            return True
        return False

    def table_exists(self, table_name):
        """
        Check if the instrument_info table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(table_name)

    def create_table_instrument_info(self):
        """
        Create the tse_instrument_info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists(TseClientInstrumentInfo.__tablename__):
            try:
                self.logger.info("Creating table...")
                TseClientInstrumentInfo.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def create_table_share_info(self):
        """
        Create the tse_instrument_info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists(TseClientShareInfo.__tablename__):
            try:
                self.logger.info("Creating table...")
                TseClientShareInfo.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def create_table_closing_price_info_adjusted(self):
        """
        Create the closing_price_info_adjusted table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists(ClosingPriceInfoAdjusted.__tablename__):
            try:
                self.logger.info("Creating table...")
                ClosingPriceInfoAdjusted.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def add_or_update_closing_price_adjusted(self, item):
        existing_record = self.session.query(ClosingPriceInfoAdjusted).filter_by(insCode=item.insCode, dEven=item.dEven, adjustMode=item.adjustMode).first()
        if existing_record:
            # Update existing record
            for key, value in item.__dict__.items():
                setattr(existing_record, key, value)
            self.logger.info(
                f"Closing Price Adjusted updated for insCode: {existing_record.insCode}, {existing_record.dEven}")
        else:
            # Add new record
            self.session.add(item)
            self.logger.info(f"Closing Price Adjusted saved for insCode: {item.insCode}, {item.dEven}")
        self.session.commit()

    def get_all_ins_codes(self):
        """
        Retrieves all values in the insCode column.

        Parameters:
        - session: SQLAlchemy session object

        Returns:
        - list: List of all values in the insCode column.
        """
        insCode_values = self.session.query(TseClientInstrumentInfo.insCode).all()
        return [value[0] for value in insCode_values]
