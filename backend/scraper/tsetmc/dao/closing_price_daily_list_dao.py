import time

import sqlalchemy as sa
from sqlalchemy import inspect, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.closing_price_daily_list import ClosingPriceDailyList
from backend.utils.scraper.tsetmc.utils import extractDateTime

Base = declarative_base()


class ClosingPriceDailyListDao(BaseLogger):
    def __init__(self, session: Session, engine: Engine, dynamic_tablename: str):
        super().__init__()
        """
        Initializes the ClosingPriceDailyListDao.

        Parameters:
        - session: SQLAlchemy session object
        - dynamic_tablename: Dynamic table name for ClosingPriceDailyList
        """
        self.engine = engine
        self.session = session
        self.dynamic_tablename = dynamic_tablename

        # Set the dynamic table name for ClosingPriceDailyList
        ClosingPriceDailyList.__table__.name = dynamic_tablename

    def save_closing_price_daily_list(self, data):
        """
        Saves a new closing price daily list entry.

        Parameters:
        - data (dict): Dictionary containing closing price daily list data.

        Returns:
        - datetime: Saved closing price daily list entry's datetime
        """
        data["datetime_str"] = extractDateTime(data["hEven"], data["dEven"])
        closing_price_daily_list = ClosingPriceDailyList(**data)
        self.session.add(closing_price_daily_list)
        self.session.commit()
        self.logger.info(f"Closing price daily list entry saved: {closing_price_daily_list.datetime_str}")
        return closing_price_daily_list.datetime_str

    def get_all_closing_price_daily_list_entries(self):
        """
        Retrieves all closing price daily list entries.

        Returns:
        - list: List of all closing price daily list entries.
        """
        return self.session.query(ClosingPriceDailyList).all()

    def get_closing_price_daily_list_by_datetime(self, datetime):
        """
        Retrieves a closing price daily list entry by its datetime.

        Parameters:
        - datetime: Datetime of the closing price daily list entry to retrieve.

        Returns:
        - ClosingPriceDailyList or None: Retrieved closing price daily list entry or None if not found.
        """
        return self.get_closing_price_daily_list_by_datetime_and_table(self.dynamic_tablename, datetime)

    def update_closing_price_daily_list(self, data):
        """
        Updates a closing price daily list entry.

        Parameters:
        - datetime: Datetime of the closing price daily list entry to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - datetime: Updated closing price daily list entry's datetime
        """
        datetime = extractDateTime(data["hEven"], data["dEven"])

        existing_record = self.get_closing_price_daily_list_by_datetime(datetime)
        if existing_record is not None:
            for key, value in data.items():
                setattr(existing_record, key, value)

            self.session.commit()
            self.logger.info(f"Closing price daily list entry updated: {datetime}")
            return existing_record.datetime_str
        else:
            return self.save_closing_price_daily_list(data)

    def delete_closing_price_daily_list_by_datetime(self, datetime):
        """
        Deletes a closing price daily list entry by its datetime.

        Parameters:
        - datetime: Datetime of the closing price daily list entry to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        closing_price_daily_list = self.session.query(ClosingPriceDailyList).filter_by(datetime_str=datetime).first()
        if closing_price_daily_list:
            self.session.delete(closing_price_daily_list)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the closing_price_daily_list table exists in the database.

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
                ClosingPriceDailyList.__table__.create(self.session.bind)
                self.logger.info(f"Table created: {self.dynamic_tablename}")
                time.sleep(0.5)
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info(f"Table {self.dynamic_tablename} already exists. ")
        return False

    def get_closing_price_daily_list_by_datetime_and_table(self, table_name, datetime_str):
        """
        Retrieves a closing price daily list entry from a specific table by its datetime.

        Parameters:
        - table_name: Name of the table to query.
        - datetime_str: Datetime of the closing price daily list entry to retrieve.

        Returns:
        - ClosingPriceDailyList or None: Retrieved closing price daily list entry or None if not found.
        """
        try:
            query = f"EXEC GetClosingPriceDailyListByDatetime @table_name='{table_name}', @datetime_str='{datetime_str}'"
            result = self.session.execute(sa.text(query)).fetchone()

            if result:
                # Convert Row to a dictionary
                result_dict = dict(result._mapping.items())
                # Assuming ClosingPriceDailyList class has a constructor that accepts **result_dict
                return ClosingPriceDailyList(**result_dict)
            else:
                return None
        except Exception as e:
            self.logger.exception(f"Error executing stored procedure: {e}")
            return None

    def get_closing_price_daily_list_last_30_items(self):
        """
        Retrieves a closing price daily list entry last 30 items based on datetime_str.

        Returns:
        - list: Retrieved closing price daily list entry last 30 items.
        """
        try:
            query = f"EXEC GetRecentItemsByDatetime @table_name='{self.dynamic_tablename}'"
            result = self.session.execute(sa.text(query)).fetchall()

            if result:
                # Get the column names from the result metadata
                column_names = ClosingPriceDailyList.columns

                # Create a list of dictionaries where keys are column names and values are row elements
                row_dicts = [dict(zip(column_names, row)) for row in result]

                # Create a list of ClosingPriceDailyList instances from the dictionaries
                result_list = [ClosingPriceDailyList(**row_dict) for row_dict in row_dicts]

                return result_list
            else:
                return None
        except Exception as e:
            self.logger.exception(f"Error executing stored procedure: {e}")
            return None
