from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.realtimedata.dao.income_statement_dao import IncomeStatementDao  # Update import


class IncomeStatementService:  # Update class name
    def __init__(self, dynamic_tablename):
        """
        Initializes the IncomeStatementService.

        Parameters:
        - dynamic_tablename: Dynamic table name for IncomeStatement
        """
        # Creating the SQLAlchemy engine
        self.engine = create_engine(SQL_SERVER_URL.replace("cm", "realtime"))
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.income_statement_dao = IncomeStatementDao(self.session, self.engine,
                                                       dynamic_tablename)  # Update dao object

    def save_income_statement_entry(self, data):  # Update method name
        """
        Saves a new IncomeStatement entry.

        Parameters:
        - data (dict): Dictionary containing IncomeStatement data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        return self.income_statement_dao.save_income_statement_entry(data)  # Update method call

    def get_all_income_statement_entries(self):  # Update method name
        """
        Retrieves all IncomeStatement entries.

        Returns:
        - list: List of all IncomeStatement entries.
        """
        return self.income_statement_dao.get_all_income_statement_entries()  # Update method call

    def update_income_statement_entry(self, data):  # Update method name
        """
        Updates a IncomeStatement entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        return self.income_statement_dao.update_income_statement_entry(data)  # Update method call

    def delete_all_income_statement_entries(self):  # Update method name
        """
        Deletes all entries from the IncomeStatement table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.income_statement_dao.delete_all_income_statement_entries()  # Update method call

    def table_exists(self):
        """
        Check if the IncomeStatement table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.income_statement_dao.table_exists()  # Update method call

    def create_table(self):
        """
        Create the desired table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.income_statement_dao.create_table()  # Update method call
