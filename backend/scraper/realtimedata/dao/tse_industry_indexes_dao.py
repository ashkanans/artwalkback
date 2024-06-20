from sqlalchemy import inspect
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.realtimedata.model.tse_industry_indexes import TseIndustryIndexes  # Update import


class TseIndustryIndexesDao(BaseLogger):  # Update class name
    def __init__(self, session: Session, engine):
        super().__init__()
        """
        Initializes the TseIndustryIndexesDao.

        Parameters:
        - session: SQLAlchemy session object
        - engine: SQLAlchemy engine object
        """
        self.session = session
        self.engine = engine

    def save_tse_industry_indexes_entry(self, data):  # Update method name
        """
        Saves a new TseIndustryIndexes entry.

        Parameters:
        - data (dict): Dictionary containing TseIndustryIndexes data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        try:
            tse_industry_indexes_entry = TseIndustryIndexes(data)  # Update model object
            self.session.add(tse_industry_indexes_entry)
            self.session.commit()
            self.logger.info(f"Saved TseIndustryIndexes row: {data}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving TseIndustryIndexes entry: {e}")
            self.session.rollback()
            return False

    def get_all_tse_industry_indexes_entries(self):  # Update method name
        """
        Retrieves all TseIndustryIndexes entries.

        Returns:
        - list: List of all TseIndustryIndexes entries.
        """
        return self.session.query(TseIndustryIndexes).all()  # Update model object

    def update_tse_industry_indexes_entry(self, data):  # Update method name
        """
        Updates a TseIndustryIndexes entry.

        Parameters:
        - entry_id: ID of the TseIndustryIndexes entry to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        try:
            self.save_tse_industry_indexes_entry(data)  # Update method call
        except Exception as e:
            self.logger.error(f"Error updating TseIndustryIndexes entry: {e}")
            self.session.rollback()
            return False

    def delete_all_tse_industry_indexes_entries(self):  # Update method name
        """
        Deletes all entries from the TseIndustryIndexes table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        try:
            self.session.execute(TseIndustryIndexes.__table__.delete())  # Update model object

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error deleting all TseIndustryIndexes entries: {e}")
            self.session.rollback()
            return False

    def table_exists(self):
        """
        Check if the TseIndustryIndexes table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.engine)
        return inspector.has_table(TseIndustryIndexes.__tablename__)

    def create_table(self):
        """
        Create the desired table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                TseIndustryIndexes.__table__.create(self.session.bind)  # Update model object
                self.logger.info(f"Table created: {TseIndustryIndexes.__tablename__}")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info(f"Table {TseIndustryIndexes.__tablename__} already exists. ")
        return False
