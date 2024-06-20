from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tgju.model.profiles import Profiles

Base = declarative_base()


class ProfilesDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        """
        Initializes the ProfilesDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_tgju_profile(self, data):
        """
        Saves a new tgju profile.

        Parameters:
        - data (dict): Dictionary containing tgju profile data.

        Returns:
        - Profiles: Saved tgju profile object.
        """
        tgju_profile = Profiles(**data)
        self.session.add(tgju_profile)
        self.session.commit()
        self.logger.info(f"Saved tgju profile entry with symbol: {tgju_profile.Symbol}")
        return tgju_profile

    def get_all_tgju_profiles(self):
        """
        Retrieves all tgju profiles.

        Returns:
        - list: List of all tgju profiles.
        """
        return self.session.query(Profiles).all()

    def get_tgju_profile_by_id(self, tgju_profile_id):
        """
        Retrieves a tgju profile by its ID.

        Parameters:
        - tgju_profile_id (str): Tgju profile ID to retrieve.

        Returns:
        - Profiles or None: Retrieved tgju profile or None if not found.
        """
        return self.session.query(Profiles).filter_by(Id=tgju_profile_id).first()

    def update_tgju_profile(self, data):
        """
        Updates a tgju profile.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - Profiles or None: Updated tgju profile object or None if not found.
        """
        existing_record = self.get_tgju_profile_by_symbol(data.get("Symbol"))

        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)
            self.session.commit()
            self.logger.info(f"Updated tgju profile entry with symbol: {existing_record.Symbol}")
            return existing_record.Symbol
        else:
            return self.save_tgju_profile(data)

    def delete_tgju_profile(self, tgju_profile_id):
        """
        Deletes a tgju profile by its ID.

        Parameters:
        - tgju_profile_id (str): Tgju profile ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        tgju_profile = self.session.query(Profiles).filter_by(Id=tgju_profile_id).first()
        if tgju_profile:
            self.session.delete(tgju_profile)
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
        return inspector.has_table(Profiles.__tablename__, schema='tgju')

    def create_table(self):
        """
        Create the tgju_profiles table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                Profiles.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_tgju_profile_by_symbol(self, tgju_profile_symbol):
        """
        Retrieves a tgju profile by its ID.

        Parameters:
        - tgju_profile_id (str): Tgju profile ID to retrieve.

        Returns:
        - Profiles or None: Retrieved tgju profile or None if not found.
        """
        return self.session.query(Profiles).filter_by(Symbol=tgju_profile_symbol).first()

    def get_list_of_symbols(self):
        """
        Retrieves a list of tgju profiles symbols.

        Returns:
        - List or None: Retrieved list of tgju profiles symbols or None if not found.
        """
        symbols = self.session.query(Profiles.Symbol).all()
        symbol_list = [symbol[0] for symbol in symbols]
        return symbol_list

    def update_by_persian_title(self, tgju_symbol, text_content):

        profile = self.get_tgju_profile_by_symbol(tgju_symbol)
        profile.NameEn = text_content
        self.logger.info(f"Tgju profile {tgju_symbol} symbols with value {text_content}")
        self.session.commit()

    def get_tgju_profile_by_nameFa(self, nameFa):

        return self.session.query(Profiles).filter_by(NameFa=nameFa).first()
