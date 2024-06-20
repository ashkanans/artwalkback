from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.realtimedata.dao.monthly_performance_dao import MonthlyPerformanceDao  # Update import


class MonthlyPerformanceService:  # Update class name
    def __init__(self, dynamic_tablename):
        """
        Initializes the MonthlyPerformanceService.

        Parameters:
        - dynamic_tablename: Dynamic table name for MonthlyPerformance
        """
        # Creating the SQLAlchemy engine
        self.engine = create_engine(SQL_SERVER_URL.replace("cm", "realtime"))
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.monthly_performance_dao = MonthlyPerformanceDao(self.session, self.engine,
                                                             dynamic_tablename)  # Update dao object

    def save_monthly_performance_entry(self, data):  # Update method name
        """
        Saves a new MonthlyPerformance entry.

        Parameters:
        - data (dict): Dictionary containing MonthlyPerformance data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        return self.monthly_performance_dao.save_monthly_performance_entry(data)  # Update method call

    def get_all_monthly_performance_entries(self):  # Update method name
        """
        Retrieves all MonthlyPerformance entries.

        Returns:
        - list: List of all MonthlyPerformance entries.
        """
        return self.monthly_performance_dao.get_all_monthly_performance_entries()  # Update method call

    def update_monthly_performance_entry(self, data):  # Update method name
        """
        Updates a MonthlyPerformance entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        return self.monthly_performance_dao.update_monthly_performance_entry(data)  # Update method call

    def delete_all_monthly_performance_entries(self):  # Update method name
        """
        Deletes all entries from the MonthlyPerformance table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.monthly_performance_dao.delete_all_monthly_performance_entries()  # Update method call

    def table_exists(self):
        """
        Check if the MonthlyPerformance table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.monthly_performance_dao.table_exists()  # Update method call

    def create_table(self):
        """
        Create the desired table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.monthly_performance_dao.create_table()  # Update method call

    def delete_all_final_mpr_entries(self):
        """
        Deletes all entries from the MonthlyPerformance table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.monthly_performance_dao.delete_all_final_mpr_entries()
