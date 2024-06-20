import datetime

import jdatetime
from sqlalchemy import inspect

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tgju.model.profiles_summary import ProfilesSummary
from backend.utils.scraper.tgju.utils import extract_number_from_span


class ProfilesSummaryDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        """
        Initializes the ProfilesSummaryDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_profile_summary(self, data):
        """
        Saves a new profile summary.

        Parameters:
        - data (dict): Dictionary containing profile summary data.

        Returns:
        - ProfilesSummary: Saved profile summary object.
        """
        profile_summary = ProfilesSummary(data)
        self.session.add(profile_summary)
        self.session.commit()
        self.logger.info(f"Saved profile summary entry with ID: {profile_summary.PrKey}")
        return profile_summary

    def get_all_profile_summaries(self):
        """
        Retrieves all profile summaries.

        Returns:
        - list: List of all profile summaries.
        """
        return self.session.query(ProfilesSummary).all()

    def update_profile_summary(self, data):
        """
        Updates a profile summary.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - ProfilesSummary or None: Updated profile summary object or None if not found.
        """
        date = datetime.datetime.strptime(data[7], '%Y/%m/%d').date()
        key = f"{data[0]} - {date}"
        if (key == "nima_buy_usd - 2022-07-23"):
            a = 1
        existing_record = self.get_profile_summary_by_prkey(key)

        if existing_record:

            existing_record.Symbol = data[0]
            existing_record.Opening = data[1]
            existing_record.Minimum = data[2]
            existing_record.Maximum = data[3]
            existing_record.Closing = data[4]
            existing_record.Change_Amount = extract_number_from_span(data[5])
            existing_record.Percentage_Change = extract_number_from_span(data[6])
            existing_record.Date_Gregorian = datetime.datetime.strptime(data[7], '%Y/%m/%d').date()
            existing_record.Date_Solar = str(jdatetime.date.fromgregorian(day=existing_record.Date_Gregorian.day,
                                                                          month=existing_record.Date_Gregorian.month,
                                                                          year=existing_record.Date_Gregorian.year))

            self.session.commit()
            self.logger.info(f"Updated profile summary entry with ID: {existing_record.PrKey}")
            return existing_record.Symbol
        else:
            return self.save_profile_summary(data)

    def delete_profile_summary(self, symbol):
        """
        Deletes a profile summary by its symbol.

        Parameters:
        - symbol (str): Profile summary ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        profile_summary = self.session.query(ProfilesSummary).filter_by(Symbol=symbol).first()
        if profile_summary:
            self.session.delete(profile_summary)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(ProfilesSummary.__tablename__, schema='tgju')

    def create_table(self):
        """
        Create the profiles_summary table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                ProfilesSummary.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info(f"Table {ProfilesSummary.__tablename__} created.")
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_profile_summary_by_prkey(self, key):
        """
        Retrieves a profile summary by its key.

        Parameters:
        - key (str): Profile summary key to retrieve.

        Returns:
        - ProfilesSummary or None: Retrieved profile summary or None if not found.
        """
        return self.session.query(ProfilesSummary).filter_by(PrKey=key).first()

    def get_first_price_by_symbol_by_year(self, symbol, year):
        """
        Get the closing price of the earliest row for a given symbol and year.

        Parameters:
        - symbol (str): Symbol for which to retrieve the price.
        - year (str): Year for which to retrieve the price.

        Returns:
        - float or None: Closing price of the earliest row for the given symbol and year, or None if not found.
        """
        try:
            # Query the database for rows matching the given symbol and year, ordered by Date_Gregorian in ascending order
            result = (
                self.session.query(ProfilesSummary)
                .filter(ProfilesSummary.Symbol == symbol, ProfilesSummary.Date_Solar.like(f'{year}%'))
                .order_by(ProfilesSummary.Date_Gregorian)
                .first()
            )

            # If a result is found, return the closing price; otherwise, return None
            return result.Closing if result else None

        except Exception as e:
            # Handle exceptions as per your application's requirements
            print(f"Error in get_first_price_by_symbol_by_year: {e}")
            return None
