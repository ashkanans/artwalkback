from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.cbi.model.inflation_rate_yearly import InflationRateYearly
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class InflationRateYearlyDao(BaseLogger):
    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the InflationRateYearlyDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_inflation_rate_yearly(self, data):
        """
        Saves a new yearly inflation rate entry.

        Parameters:
        - data (dict): Dictionary containing yearly inflation data.

        Returns:
        - int: Saved yearly inflation entry's ID
        """
        inflation_rate_yearly = InflationRateYearly(**data)
        self.session.add(inflation_rate_yearly)
        self.session.commit()
        self.logger.info(f"Saved yearly inflation rate entry with ID: {inflation_rate_yearly.Year}")
        return inflation_rate_yearly.Year

    def get_all_inflation_rate_yearly_entries(self):
        """
        Retrieves all instrument info entries.

        Returns:
        - list: List of all instrument info entries.
        """
        return self.session.query(InflationRateYearly).all()

    def get_inflation_rate_yearly_by_id(self, id):
        """
        Retrieves a yearly inflation rate entry by its ID.

        Parameters:
        - id (integer): yearly inflation rate entry ID to retrieve.

        Returns:
        - InflationRateYearly or None: Retrieved yearly inflation rate entry or None if not found.
        """
        return self.session.query(InflationRateYearly).filter_by(Id=id).first()

    def get_inflation_rate_yearly_by_year(self, year):
        """
        Retrieves a yearly inflation rate entry by year.

        Parameters:
        - id (integer): yearly inflation rate entry ID to retrieve.

        Returns:
        - InflationRateYearly or None: Retrieved yearly inflation rate entry or None if not found.
        """
        return self.session.query(InflationRateYearly).filter_by(Year=year).first()

    def update_inflation_rate_yearly(self, data):
        """
        Updates a yearly inflation rate entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated yearly inflation rate entry's ID
        """
        try:

            existing_record = self.get_inflation_rate_yearly_by_year(data.get("Year"))
            if existing_record:
                for key, value in data.items():
                    setattr(existing_record, key, value)

                self.session.commit()
                self.logger.info(f"Updated yearly inflation rate entry with ID: {existing_record.Year}")
                return existing_record.Year
            else:
                return self.save_inflation_rate_yearly(data)
        except NoResultFound:
            return self.save_inflation_rate_yearly(data)

    def delete_inflation_rate_yearly_by_id(self, id):
        """
        Deletes a yearly inflation rate entry by its ID.

        Parameters:
        - insCode (str): yearly inflation rate entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        inflation_rate_yearly = self.session.query(InflationRateYearly).filter_by(Id=id).first()
        if inflation_rate_yearly:
            self.session.delete(inflation_rate_yearly)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the inflation_rate_yearly table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(InflationRateYearly.__tablename__)

    def create_table(self):
        """
        Create the cbi_inflation_rate_yearly table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table InflationRateYearly...")
                InflationRateYearly.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("InflationRateYearly Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table InflationRateYearly: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("InflationRateYearly Table already exists.")
        return False
