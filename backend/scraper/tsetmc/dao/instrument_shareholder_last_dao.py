import time

import sqlalchemy as sa
from sqlalchemy import inspect, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.instrument_shareholder_last import InstrumentShareholderLast
from backend.utils.scraper.tsetmc.utils import extractDateTime

Base = declarative_base()


class InstrumentShareholderLastDao(BaseLogger):
    def __init__(self, session: Session, engine: Engine, dynamic_tablename: str):
        super().__init__()
        """
        Initializes the InstrumentShareholderLastDao.

        Parameters:
        - session: SQLAlchemy session object
        - dynamic_tablename: Dynamic table name for InstrumentShareholderLast
        """
        self.engine = engine
        self.session = session
        self.dynamic_tablename = dynamic_tablename

        # Set the dynamic table name for InstrumentShareholderLast
        InstrumentShareholderLast.__table__.name = dynamic_tablename

    def save_instrument_shareholder_last(self, data):
        """
        Saves a new instrument shareholder last entry.

        Parameters:
        - data (dict): Dictionary containing instrument shareholder last data.

        Returns:
        - datetime: Saved instrument shareholder last entry's datetime
        """
        data["datetime_str"] = extractDateTime(data["hEven"], data["dEven"])
        instrument_shareholder_last = InstrumentShareholderLast(**data)
        self.session.add(instrument_shareholder_last)
        self.session.commit()
        self.logger.info(f"Instrument shareholder last entry saved: {instrument_shareholder_last.datetime_str}")
        return instrument_shareholder_last.datetime_str

    def get_all_instrument_shareholder_last_entries(self):
        """
        Retrieves all instrument shareholder last entries.

        Returns:
        - list: List of all instrument shareholder last entries.
        """
        return self.session.query(InstrumentShareholderLast).all()

    def get_instrument_shareholder_last_by_datetime(self, datetime):
        """
        Retrieves an instrument shareholder last entry by its datetime.

        Parameters:
        - datetime: Datetime of the instrument shareholder last entry to retrieve.

        Returns:
        - InstrumentShareholderLast or None: Retrieved instrument shareholder last entry or None if not found.
        """
        return self.get_instrument_shareholder_last_by_datetime_and_table(self.dynamic_tablename, datetime)

    def update_instrument_shareholder_last(self, data):
        """
        Updates an instrument shareholder last entry.

        Parameters:
        - datetime: Datetime of the instrument shareholder last entry to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - datetime: Updated instrument shareholder last entry's datetime
        """
        datetime = extractDateTime(data["hEven"], data["dEven"])

        existing_record = self.get_instrument_shareholder_last_by_datetime(datetime)
        if existing_record is not None:
            for key, value in data.items():
                setattr(existing_record, key, value)

            self.session.commit()
            self.logger.info(f"Instrument shareholder last entry updated: {datetime}")
            return existing_record.datetime_str
        else:
            return self.save_instrument_shareholder_last(data)

    def delete_instrument_shareholder_last_by_datetime(self, datetime):
        """
        Deletes an instrument shareholder last entry by its datetime.

        Parameters:
        - datetime: Datetime of the instrument shareholder last entry to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        instrument_shareholder_last = self.session.query(InstrumentShareholderLast).filter_by(datetime_str=datetime).first()
        if instrument_shareholder_last:
            self.session.delete(instrument_shareholder_last)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the instrument_shareholder_last table exists in the database.

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
                InstrumentShareholderLast.__table__.create(self.session.bind)
                self.logger.info(f"Table created: {self.dynamic_tablename}")
                time.sleep(0.5)
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info(f"Table {self.dynamic_tablename} already exists. ")
        return False

    def get_instrument_shareholder_last_by_datetime_and_table(self, table_name, datetime_str):
        """
        Retrieves an instrument shareholder last entry from a specific table by its datetime.

        Parameters:
        - table_name: Name of the table to query.
        - datetime_str: Datetime of the instrument shareholder last entry to retrieve.

        Returns:
        - InstrumentShareholderLast or None: Retrieved instrument shareholder last entry or None if not found.
        """
        try:
            query = f"EXEC GetInstrumentShareholderLastByDatetime @table_name='{table_name}', @datetime_str='{datetime_str}'"
            result = self.session.execute(sa.text(query)).fetchone()

            if result:
                # Convert Row to a dictionary
                result_dict = dict(result._mapping.items())
                # Assuming InstrumentShareholderLast class has a constructor that accepts **result_dict
                return InstrumentShareholderLast(**result_dict)
            else:
                return None
        except Exception as e:
            self.logger.exception(f"Error executing stored procedure: {e}")
            return None

    def get_instrument_shareholder_last_last_30_items(self):
        """
        Retrieves an instrument shareholder last entry last 30 items based on datetime_str.

        Returns:
        - list: Retrieved instrument shareholder last entry last 30 items.
        """
        try:
            query = f"EXEC GetRecentItemsByDatetime @table_name='{self.dynamic_tablename}'"
            result = self.session.execute(sa.text(query)).fetchall()

            if result:
                # Get the column names from the result metadata
                column_names = InstrumentShareholderLast.columns

                # Create a list of dictionaries where keys are column names and values are row elements
                row_dicts = [dict(zip(column_names, row)) for row in result]

                # Create a list of InstrumentShareholderLast instances from the dictionaries
                result_list = [InstrumentShareholderLast(**row_dict) for row_dict in row_dicts]

                return result_list
            else:
                return None
        except Exception as e:
            self.logger.exception(f"Error executing stored procedure: {e}")
            return None