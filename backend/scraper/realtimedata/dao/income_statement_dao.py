from sqlalchemy import inspect
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.realtimedata.model.income_statement import IncomeStatement  # Update import


class IncomeStatementDao(BaseLogger):  # Update class name
    def __init__(self, session: Session, engine, dynamic_tablename: str):
        super().__init__()
        """
        Initializes the IncomeStatementDao.

        Parameters:
        - session: SQLAlchemy session object
        - engine: SQLAlchemy engine object
        - dynamic_tablename: Dynamic table name for IncomeStatement
        """
        self.session = session
        self.engine = engine
        self.dynamic_tablename = dynamic_tablename

        # Set the dynamic table name for IncomeStatement
        IncomeStatement.__table__.name = dynamic_tablename

    def save_income_statement_entry(self, data):  # Update method name
        """
        Saves a new IncomeStatement entry.

        Parameters:
        - data (dict): Dictionary containing IncomeStatement data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        try:
            income_statement_entry = IncomeStatement(data)  # Update model object
            self.session.add(income_statement_entry)
            self.session.commit()
            self.logger.info(f"Saved IncomeStatement row: {data}")
            return True
        except Exception as e:
            self.logger.error(f"Error saving IncomeStatement entry: {e}")
            self.session.rollback()
            return False

    def get_all_income_statement_entries(self):  # Update method name
        """
        Retrieves all IncomeStatement entries.

        Returns:
        - list: List of all IncomeStatement entries.
        """
        return self.session.query(IncomeStatement).all()  # Update model object

    def update_income_statement_entry(self, data):  # Update method name
        """
        Updates a IncomeStatement entry.

        Parameters:
        - entry_id: ID of the IncomeStatement entry to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        try:
            self.save_income_statement_entry(data)  # Update method call
        except Exception as e:
            self.logger.error(f"Error updating IncomeStatement entry: {e}")
            self.session.rollback()
            return False

    def delete_all_income_statement_entries(self):  # Update method name
        """
        Deletes all entries from the IncomeStatement table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        try:
            self.session.execute(IncomeStatement.__table__.delete())  # Update model object

            self.session.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error deleting all IncomeStatement entries: {e}")
            self.session.rollback()
            return False

    def table_exists(self):
        """
        Check if the IncomeStatement table exists in the database.

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
                IncomeStatement.__table__.create(self.session.bind)  # Update model object
                self.logger.info(f"Table created: {self.dynamic_tablename}")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info(f"Table {self.dynamic_tablename} already exists. ")
        return False
