from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.realtimedata.dao.final_mpr_dao import FinalMprDao


class FinalMprService:
    def __init__(self, dynamic_tablename):
        """
        Initializes the FinalMprService.

        Parameters:
        - dynamic_tablename: Dynamic table name for FinalMpr
        """
        # Creating the SQLAlchemy engine
        self.engine = create_engine(SQL_SERVER_URL.replace("cm", "realtime"))
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.final_mpr_dao = FinalMprDao(self.session, self.engine, dynamic_tablename)

    def save_final_mpr_entry(self, data):
        """
        Saves a new FinalMpr entry.

        Parameters:
        - data (dict): Dictionary containing FinalMpr data.

        Returns:
        - bool: True if the entry is saved successfully, False otherwise.
        """
        return self.final_mpr_dao.save_final_mpr_entry(data)

    def get_all_final_mpr_entries(self):
        """
        Retrieves all FinalMpr entries.

        Returns:
        - list: List of all FinalMpr entries.
        """
        return self.final_mpr_dao.get_all_final_mpr_entries()

    def update_final_mpr_entry(self, data):
        """
        Updates a FinalMpr entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - bool: True if the entry is updated successfully, False otherwise.
        """
        return self.final_mpr_dao.update_final_mpr_entry(data)

    def delete_all_final_mpr_entries(self):
        """
        Deletes all entries from the FinalMpr table.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.final_mpr_dao.delete_all_final_mpr_entries()

    def table_exists(self):
        """
        Check if the FinalMpr table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        return self.final_mpr_dao.table_exists()

    def create_table(self):
        """
        Create the desired table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.final_mpr_dao.create_table()
