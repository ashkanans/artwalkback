from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tgju.model.profiles_current import TgjuCurrentProfiles

Base = declarative_base()


class CurrentProfilesDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        """
        Initializes the TgjuCurrentProfilesDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_tgju_current_profile(self, data):
        """
        Saves a new tgju current profile.

        Parameters:
        - data (dict): Dictionary containing tgju current profile data.

        Returns:
        - TgjuCurrentProfiles: Saved tgju current profile object.
        """
        tgju_current_profile = TgjuCurrentProfiles(**data)
        self.session.add(tgju_current_profile)
        self.session.commit()
        self.logger.info(f"Saved tgju current profile entry with symbol: {tgju_current_profile.Symbol}")
        return tgju_current_profile

    def get_all_tgju_current_profiles(self):
        """
        Retrieves all tgju current profiles.

        Returns:
        - list: List of all tgju current profiles.
        """
        return self.session.query(TgjuCurrentProfiles).all()

    def get_tgju_current_profile_by_symbol(self, symbol):
        """
        Retrieves a tgju current profile by its symbol.

        Parameters:
        - symbol (str): Tgju current profile symbol to retrieve.

        Returns:
        - TgjuCurrentProfiles or None: Retrieved tgju current profile or None if not found.
        """
        return self.session.query(TgjuCurrentProfiles).filter_by(Symbol=symbol).first()

    def update_tgju_current_profile(self, data):
        """
        Updates a tgju current profile.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - TgjuCurrentProfiles or None: Updated tgju current profile object or None if not found.
        """
        existing_record = self.get_tgju_current_profile_by_symbol(data.get("Symbol"))

        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)
            self.session.commit()
            self.logger.info(f"Updated tgju current profile entry with symbol: {existing_record.Symbol}")
            return existing_record.Symbol
        else:
            return self.save_tgju_current_profile(data)

    def delete_tgju_current_profile(self, symbol):
        """
        Deletes a tgju current profile by its symbol.

        Parameters:
        - symbol (str): Tgju current profile symbol to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        tgju_current_profile = self.session.query(TgjuCurrentProfiles).filter_by(Symbol=symbol).first()
        if tgju_current_profile:
            self.session.delete(tgju_current_profile)
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
        return inspector.has_table(TgjuCurrentProfiles.__tablename__, schema='tgju')

    def create_table(self):
        """
        Create the tgju_current_profiles table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                TgjuCurrentProfiles.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False
