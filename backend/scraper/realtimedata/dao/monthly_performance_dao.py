from sqlalchemy import inspect
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.realtimedata.model.monthly_performance import MonthlyPerformance  # Update import


class MonthlyPerformanceDao(BaseLogger):  # Update class name
    def __init__(self, session: Session, engine, dynamic_tablename: str):
        super().__init__()
        """
        Initializes the MonthlyPerformanceDao.

        Parameters:
        - session: SQLAlchemy session object
        - engine: SQLAlchemy engine object
        - dynamic_tablename: Dynamic table name for MonthlyPerformance
        """
        self.session = session
        self.engine = engine
        self.dynamic_tablename = dynamic_tablename

        # Set the dynamic table name for MonthlyPerformance
        MonthlyPerformance.__table__.name = dynamic_tablename

    def save_monthly_performance_entry(self, data):  # Update method name
        """
        Saves a new MonthlyPerformance entry.

        Parameters:
        - data (dict): Dictionary containing MonthlyPerformance data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        try:
            monthly_performance_entry = MonthlyPerformance(data)  # Update model object
            self.session.add(monthly_performance_entry)
            self.session.commit()
            self.logger.info(f"Saved MonthlyPerformance row: {data}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving MonthlyPerformance entry: {e}")
            self.session.rollback()
            return False

    def get_all_monthly_performance_entries(self):  # Update method name
        """
        Retrieves all MonthlyPerformance entries.

        Returns:
        - list: List of all MonthlyPerformance entries.
        """
        return self.session.query(MonthlyPerformance).all()  # Update model object

    def update_monthly_performance_entry(self, data):  # Update method name
        """
        Updates a MonthlyPerformance entry.

        Parameters:
        - entry_id: ID of the MonthlyPerformance entry to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        try:
            self.save_monthly_performance_entry(data)  # Update method call
        except Exception as e:
            self.logger.error(f"Error updating MonthlyPerformance entry: {e}")
            self.session.rollback()
            return False

    def delete_all_monthly_performance_entries(self):  # Update method name
        """
        Deletes all entries from the MonthlyPerformance table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        try:
            self.session.execute(MonthlyPerformance.__table__.delete())  # Update model object

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error deleting all MonthlyPerformance entries: {e}")
            self.session.rollback()
            return False

    def table_exists(self):
        """
        Check if the MonthlyPerformance table exists in the database.

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
                MonthlyPerformance.__table__.create(self.session.bind)  # Update model object
                self.logger.info(f"Table created: {self.dynamic_tablename}")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info(f"Table {self.dynamic_tablename} already exists. ")
        return False

    def delete_all_final_mpr_entries(self):
        """
        Deletes all entries from the MonthlyPerformance table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        try:
            self.session.execute(MonthlyPerformance.__table__.delete())

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error deleting all FinalMpr entries: {e}")
            self.session.rollback()
            return False
