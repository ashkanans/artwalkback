from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.instrument_state_top import InstrumentStateTop

Base = declarative_base()


class InstrumentStateTopDao(BaseLogger):

    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the InstrumentStateTopDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_instrument_state_top(self, data):
        """
               Saves a new msg by flow entry.

               Parameters:
               - data (dict): Dictionary containing closing price daily list data.

               Returns:
               - datetime: Saved closing price daily list entry's datetime
               """
        instrument_state_top = InstrumentStateTop(**data)
        self.session.add(instrument_state_top)
        self.session.commit()
        self.logger.info(f"instrument state top entry saved: {instrument_state_top.idn}")
        return instrument_state_top.idn

    def get_instrument_state_top_by_idn(self, idn):
        """
        Retrieves a instrument state top entry by its idn.

        Parameters:
        - code (str): instrument state top entry idn to retrieve.

        Returns:
        - main groups or None: Retrieved instrument state top entry or None if not found.
        """
        return self.session.query(InstrumentStateTop).filter_by(idn=idn).first()

    def get_all_instrument_state_top_entries(self):
        """
        Retrieves all instrument state top  entries.

        Returns:
        - list: List of all instrument state top  entries.
        """
        return self.session.query(InstrumentStateTop).all()

    def update_instrument_state_top(self, data):
        """
        Updates a instrument state top entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated instrument state top entry's idn
        """
        updated_ids = []

        try:
            existing_record = self.get_instrument_state_top_by_idn(data.get("idn"))
            if existing_record:
                for idn, value in data.items():
                    setattr(existing_record, idn, value)

                self.session.commit()
                self.logger.info(f"Updated instrument state top entry with idn: {existing_record.idn}")
                updated_ids.append(existing_record.idn)
            else:
                self.save_instrument_state_top(data)

        except NoResultFound:
            updated_ids.append(self.save_instrument_state_top(data))

        return updated_ids

    def delete_instrument_state_top_by_idn(self, idn):
        """
        Deletes a instrument state top entry by its idn.

        Parameters:
        - code (str): instrument state top entry idn to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        instrument_state_top = self.session.query(InstrumentStateTop).filter_by(idn=idn).first()
        if instrument_state_top:
            self.session.delete(instrument_state_top)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the instrument_state_top table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(InstrumentStateTop.__tablename__)

    def create_table(self):
        """
        Create the tse_instrument_state_top table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                InstrumentStateTop.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False
