from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.get_related_company_dao import GetRelatedCompanyDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class GetRelatedCompanyService(BaseLogger):
    def __init__(self):
        """
        Initializes the GetRelatedCompanyService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.get_related_company_dao = GetRelatedCompanyDao(session)

    def save_get_related_company(self, data):
        """
        Saves a new get related company  entry.

        Parameters:
        - data (dict): Dictionary containing get related company  data.

        Returns:
        - int: Saved get related company  entry's inscode
        """
        return self.get_related_company_dao.save_get_related_company(data)

    def get_all_get_related_company_entries(self):
        """
        Retrieves all get related company  entries.

        Returns:
        - list: List of all get related company  entries.
        """
        return self.get_related_company_dao.get_all_get_related_company_entries()

    def get_get_related_company_by_inscode(self, code):
        """
        Retrieves a get related company  entry by its inscode.

        Parameters:
        - code (str): get related company  entry inscode to retrieve.

        Returns:
        - GetRelatedCompany or None: Retrieved get related company  entry or None if not found.
        """
        return self.get_related_company_dao.get_get_related_company_by_inscode(code)

    def update_get_related_company(self, data):
        """
        Updates a get related company  entry.

        Parameters:
        - code (str): get related company  entry inscode to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated get related company  entry's inscode
        """

        return self.get_related_company_dao.update_get_related_company(data)

    def delete_get_related_company_by_inscode(self, code):
        """
        Deletes a get related company  entry by its inscode.

        Parameters:
        - code (str): get related company  entry inscode to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.get_related_company_dao.delete_get_related_company_by_inscode(code)

    def create_table(self):
        """
        Create the get related company table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.get_related_company_dao.create_table()

    def table_exists(self):
        """
        Create the get related company table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """

        return self.get_related_company_dao.table_exists()

    def get_list_data(self, inscode):
        return GetRelatedCompanyDao.get_list_data(self, inscode)
