from sqlalchemy import inspect
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.realtimedata.model.final_mpr import FinalMpr


class FinalMprDao(BaseLogger):
    def __init__(self, session: Session, engine, dynamic_tablename: str):
        super().__init__()
        """
        Initializes the FinalMprDao.

        Parameters:
        - session: SQLAlchemy session object
        - engine: SQLAlchemy engine object
        - dynamic_tablename: Dynamic table name for FinalMpr
        """
        self.session = session
        self.engine = engine
        self.dynamic_tablename = dynamic_tablename

        # Set the dynamic table name for FinalMpr
        FinalMpr.__table__.name = dynamic_tablename

    def save_final_mpr_entry(self, data):
        """
        Saves a new FinalMpr entry.

        Parameters:
        - data (dict): Dictionary containing FinalMpr data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        try:
            final_mpr_entry = FinalMpr(data)
            self.session.add(final_mpr_entry)
            self.session.commit()
            self.logger.info(f"Saved FinalMpr row: {data}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving FinalMpr entry: {e}")
            self.session.rollback()
            return False

    def get_all_final_mpr_entries(self):
        """
        Retrieves all FinalMpr entries.

        Returns:
        - list: List of all FinalMpr entries.
        """
        return self.session.query(FinalMpr).all()

    def update_final_mpr_entry(self, data):
        """
        Updates a FinalMpr entry.

        Parameters:
        - entry_id: ID of the FinalMpr entry to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        try:
            self.save_final_mpr_entry(data)
        except Exception as e:
            self.logger.error(f"Error updating FinalMpr entry: {e}")
            self.session.rollback()
            return False

    def delete_all_final_mpr_entries(self):
        """
        Deletes all entries from the FinalMpr table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        try:
            self.session.execute(FinalMpr.__table__.delete())

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error deleting all FinalMpr entries: {e}")
            self.session.rollback()
            return False

    def table_exists(self):
        """
        Check if the FinalMpr table exists in the database.

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
                FinalMpr.__table__.create(self.session.bind)
                self.logger.info(f"Table created: {self.dynamic_tablename}")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info(f"Table {self.dynamic_tablename} already exists. ")
        return False
