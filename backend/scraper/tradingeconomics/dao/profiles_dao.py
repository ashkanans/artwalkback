import re

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

from backend.scraper.tradingeconomics.model.profiles import Profiles
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class ProfilesDao(BaseLogger):
    def __init__(self, session):
        """
        Initializes the Logger.
        Initializes the ProfilesDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        super().__init__() 
        self.session = session

    def save_profiles(self, data):
        """
        Saves a new profiles.

        Parameters:
        - data (dict): Dictionary containing profiles data.

        Returns:
        - Profiles: Saved profiles object.
        """
        profiles = Profiles(**data)
        self.session.add(profiles)
        self.session.commit()
        self.logger.info(f"tradingeconomics profile saved link: {profiles.link}")
        return profiles

    def get_all_profiless(self):
        """
        Retrieves all profiless.

        Returns:
        - list: List of all profiless.
        """
        return self.session.query(Profiles).all()

    def get_all_urls(self):
        """
        Retrieves all profiless.

        Returns:
        - list: List of all profiless.
        """
        return [link[0] for link in self.session.query(Profiles.link).all()]


    def get_profiles_by_name(self, name):
        """
        Retrieves a profiles by its tracing number.

        Parameters:
        - name (int): Tracing number to retrieve.

        Returns:
        - Profiles or None: Retrieved profiles or None if not found.
        """
        return self.session.query(Profiles).filter_by(name).first()

    def update_profiles(self, data):
        """
        Updates a profiles.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - Profiles or None: Updated profiles object or None if not found.
        """
        existing_record = self.session.query(Profiles).filter_by(name=data.get("name")).first()
        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)
            self.session.commit()
            self.logger.info(f"tradingeconomics profile edited link: {existing_record.link}")
            return existing_record.name
        else:
            return self.save_profiles(data)

    def update_Profile_by_link(self, data):
        """
        Updates a profile by link.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - Profiles or None: Updated profiles object or None if not found.
        """
        existing_record = self.session.query(Profiles).filter_by(link=data.get("link")).first()

        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)
            self.session.commit()
            self.logger.info(f"tradingeconomics profile token and type added: {existing_record.link}")
            return existing_record.link
        else:
            return self.save_profiles(data)


    def delete_profiles(self, name):
        """
        Deletes a profiles by its tracing number.

        Parameters:
        - name (int): Tracing number to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        profiles = self.session.query(Profiles).filter_by(name).first()
        if profiles:
            self.session.delete(profiles)
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
        return inspector.has_table(Profiles.__tablename__)

    def create_table(self):
        """
        Create the profiless table in the database.

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
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False
