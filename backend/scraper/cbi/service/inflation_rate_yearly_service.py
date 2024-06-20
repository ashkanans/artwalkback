from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.cbi.dao.inflation_rate_yearly_dao import InflationRateYearlyDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class InflationRateYearlyService:
    def __init__(self):
        """
        Initializes the InflationRateYearlyService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.inflation_rate_yearly_dao = InflationRateYearlyDao(session)

    def save_inflation_rate_yearly(self, data):
        """
        Saves a new yearly inflation rate entry.

        Parameters:
        - data (dict): Dictionary containing yearly inflation rate data.

        Returns:
        - int: Saved yearly inflation rate entry's ID
        """
        return self.inflation_rate_yearly_dao.save_inflation_rate_yearly(data)

    def get_all_inflation_rate_yearly_entries(self):
        """
        Retrieves all yearly inflation rate entries.

        Returns:
        - list: List of all yearly inflation rate entries.
        """
        return self.inflation_rate_yearly_dao.get_all_inflation_rate_yearly_entries()

    def get_inflation_rate_yearly_by_id(self, id):
        """
        Retrieves a yearly inflation rate entry by its ID.

        Parameters:
        - id (str): yearly inflation rate entry ID to retrieve.

        Returns:
        - InflationRateYearly or None: Retrieved yearly inflation rate entry or None if not found.
        """
        return self.inflation_rate_yearly_dao.get_inflation_rate_yearly_by_id(id)

    def update_inflation_rate_yearly(self, data):
        """
        Updates a yearly inflation rate entry.

        Parameters:
        - id (str): yearly inflation rate entry ID to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated yearly inflation rate entry's ID
        """
        updated_years = []
        for item in data:
            updated_year = self.inflation_rate_yearly_dao.update_inflation_rate_yearly(item)
            updated_years.append(updated_year)

        return updated_years

    def delete_inflation_rate_yearly_by_id(self, id):
        """
        Deletes a yearly inflation rate entry by its ID.

        Parameters:
        - id (str): yearly inflation rate entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.inflation_rate_yearly_dao.delete_inflation_rate_yearly_by_id(id)

    def create_table(self):
        """
        Create the inflation_rate_yearly table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.inflation_rate_yearly_dao.create_table()

    def table_exists(self):
        """
        Create the inflation_rate_yearly table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.inflation_rate_yearly_dao.table_exists()

    def get_inflation_rate_yearly_by_year(self, year):
        return self.inflation_rate_yearly_dao.get_inflation_rate_yearly_by_year(year)
