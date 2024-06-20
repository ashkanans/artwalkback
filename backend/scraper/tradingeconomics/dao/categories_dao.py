import re

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

from backend.scraper.tradingeconomics.model.categories import Categories
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class CategoriesDao(BaseLogger):
    def __init__(self, session):
        """
        Initializes the Logger.
        Initializes the CategoriesDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        super().__init__() 
        self.session = session

    def save_categories(self, data):
        """
        Saves a new categories.

        Parameters:
        - data (dict): Dictionary containing categories data.

        Returns:
        - Categories: Saved categories object.
        """
        categories = Categories(**data)
        self.session.add(categories)
        self.session.commit()
        self.logger.info(f"tradingeconomics categories saved Name: {categories.name}")
        return categories

    def get_all_categories(self):
        """
        Retrieves all categoriess.

        Returns:
        - list: List of all categoriess.
        """
        return self.session.query(Categories).all()

    def get_all_urls(self):
        """
        Retrieves all categories.

        Returns:
        - list: List of all categories.
        """
        return [link[0] for link in self.session.query(Categories.link).all()]

    def update_categories(self, data):
        """
        Updates a categories.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - Categories or None: Updated categories object or None if not found.
        """
        existing_record = self.session.query(Categories).filter_by(name=data.get("name")).first()
        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)
            self.session.commit()
            self.logger.info(f"tradingeconomics categories edited Name: {existing_record.name}")

            return existing_record.name
        else:
            return self.save_categories(data)

    def delete_categories(self, name):
        """
        Deletes a categories by its tracing number.

        Parameters:
        - tracing_no (int): Tracing number to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        categories = self.session.query(Categories).filter_by(name).first()
        if categories:
            self.session.delete(categories)
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
        return inspector.has_table(Categories.__tablename__)

    def create_table(self):
        """
        Create the categories table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                Categories.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False
