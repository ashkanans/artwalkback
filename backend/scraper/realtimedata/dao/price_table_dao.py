from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.realtimedata.model.price_table import PriceTable

Base = declarative_base()


class PriceTableDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def save_price_table(self, data):
        """
        Saves a new price table entry.

        Parameters:
        - data (dict): Dictionary containing price table data.

        Returns:
        - PriceTable: Saved price table object.
        """
        price_table = PriceTable(**data)
        self.session.add(price_table)
        self.session.commit()
        self.logger.info(f"Saved {price_table.currency_name}")
        return price_table

    def get_all_price_tables(self):
        """
        Retrieves all price tables.

        Returns:
        - list: List of all price tables.
        """
        return self.session.query(PriceTable).all()

    def get_price_table_by_currency_name(self, currency_name):
        """
        Retrieves a price table by its currency name.

        Parameters:
        - currency_name (str): Currency name to retrieve.

        Returns:
        - PriceTable or None: Retrieved price table or None if not found.
        """
        return self.session.query(PriceTable).filter_by(currency_name=currency_name).first()

    def update_price_table(self, data):
        """
        Updates a price table.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - PriceTable or None: Updated price table object or None if not found.
        """
        existing_record = self.get_price_table_by_currency_name(data.get("currency_name"))

        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)
            self.session.commit()
            self.logger.info(f"Updated {existing_record.currency_name}")
            return existing_record
        else:
            return self.save_price_table(data)

    def delete_price_table(self, currency_name):
        """
        Deletes a price table by its currency name.

        Parameters:
        - currency_name (str): Currency name to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        price_table = self.session.query(PriceTable).filter_by(currency_name=currency_name).first()
        if price_table:
            self.session.delete(price_table)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(PriceTable.__tablename__)

    def create_table(self):
        """
        Create the price_table table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                PriceTable.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.error(f"Creating table {PriceTable.__tablename__}")
                return True
            except Exception as e:
                self.session.rollback()
                self.logger.error(f"Error while creating table {PriceTable.__tablename__}")
                return False
        return False
