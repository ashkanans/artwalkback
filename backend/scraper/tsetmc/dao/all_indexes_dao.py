from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.all_indexes import AllIndexes

Base = declarative_base()


class AllIndexesDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        """
        Initializes the AllIndexesDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_all_indexes(self, data):
        """
        Saves a new all indexes.

        Parameters:
        - data (dict): Dictionary containing all indexes data.

        Returns:
        - AllIndexes: Saved all indexes object.
        """
        all_indexes = AllIndexes(**data)
        self.session.add(all_indexes)
        self.session.commit()
        self.logger.info(f"Saved all indexes entry with ID: {all_indexes.lVal30}")
        return all_indexes

    def get_all_all_indexess(self):
        """
        Retrieves all all indexess.

        Returns:
        - list: List of all all indexess.
        """
        return self.session.query(AllIndexes).all()

    def get_all_indexes_by_name(self, all_indexes_name):
        """
        Retrieves a all indexes by its name.

        Parameters:
        - all_indexes_name (int): all indexes name to retrieve.

        Returns:
        - AllIndexes or None: Retrieved all indexes or None if not found.
        """
        return self.session.query(AllIndexes).filter_by(lVal30=all_indexes_name).first()

    def update_all_indexes(self, data):
        """
        Updates a all indexes.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - AllIndexes or None: Updated all indexes object or None if not found.
        """
        existing_record = self.get_all_indexes_by_name(data.get("lVal30"))

        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)
            self.session.commit()
            self.logger.info(f"Updated all indexes entry with ID: {existing_record.lVal30}")
            return existing_record.lVal30
        else:
            return self.save_all_indexes(data)

    def delete_all_indexes(self, all_indexes_name):
        """
        Deletes a all indexes by its name.

        Parameters:
        - all_indexes_name (int): all indexes name to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        all_indexes = self.session.query(AllIndexes).filter_by(lVal30=all_indexes_name).first()
        if all_indexes:
            self.session.delete(all_indexes)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Parameters:
        - table_name (str): The name of the table to check.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(AllIndexes.__tablename__)

    def create_table(self):
        """
        Create the tse_all_indexes table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                AllIndexes.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_data_contain_specifi_value_in_name(self, txt):
        return self.session.query(AllIndexes).filter(AllIndexes.lVal30.contains(txt)).first()
