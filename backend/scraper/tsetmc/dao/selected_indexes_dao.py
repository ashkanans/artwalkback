from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.selected_indexes import SelectedIndexes

Base = declarative_base()


class SelectedIndexesDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        """
        Initializes the SelectedIndexesDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_selected_indexes(self, data):
        """
        Saves a new selected indexes.

        Parameters:
        - data (dict): Dictionary containing selected indexes data.

        Returns:
        - SelectedIndexes: Saved selected indexes object.
        """
        selected_indexes = SelectedIndexes(**data)
        self.session.add(selected_indexes)
        self.session.commit()
        self.logger.info(f"Saved selected indexes entry with ID: {selected_indexes.lVal30}")
        return selected_indexes

    def get_all_selected_indexess(self):
        """
        Retrieves all selected indexess.

        Returns:
        - list: List of all selected indexess.
        """
        return self.session.query(SelectedIndexes).all()

    def get_selected_indexes_by_name(self, selected_indexes_name):
        """
        Retrieves a selected indexes by its name.

        Parameters:
        - selected_indexes_name (int): selected indexes name to retrieve.

        Returns:
        - SelectedIndexes or None: Retrieved selected indexes or None if not found.
        """
        return self.session.query(SelectedIndexes).filter_by(lVal30=selected_indexes_name).first()

    def update_selected_indexes(self, data):
        """
        Updates a selected indexes.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - SelectedIndexes or None: Updated selected indexes object or None if not found.
        """
        existing_record = self.get_selected_indexes_by_name(data.get("lVal30"))

        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)
            self.session.commit()
            self.logger.info(f"Updated selected indexes entry with ID: {existing_record.lVal30}")
            return existing_record.lVal30
        else:
            return self.save_selected_indexes(data)

    def delete_selected_indexes(self, selected_indexes_name):
        """
        Deletes a selected indexes by its name.

        Parameters:
        - selected_indexes_name (int): selected indexes name to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        selected_indexes = self.session.query(SelectedIndexes).filter_by(lVal30=selected_indexes_name).first()
        if selected_indexes:
            self.session.delete(selected_indexes)
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
        return inspector.has_table(SelectedIndexes.__tablename__)

    def create_table(self):
        """
        Create the tse_selected_indexes table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                SelectedIndexes.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False
