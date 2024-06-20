from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.prepared_data import PreparedData

Base = declarative_base()


class PreparedDataDao(BaseLogger):

    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the PreparedDataDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_prepared_data(self, data):
        """
               Saves a new msg by flow entry.

               Parameters:
               - data (dict): Dictionary containing closing price daily list data.

               Returns:
               - datetime: Saved closing price daily list entry's datetime
               """
        prepared_data = PreparedData(**data)
        self.session.add(prepared_data)
        self.session.commit()
        self.logger.info(f"prepared data entry saved: {prepared_data.id}")
        return prepared_data.id

    def get_prepared_data_by_id(self, id):
        """
        Retrieves a prepared data entry by its id.

        Parameters:
        - code (str): prepared data entry id to retrieve.

        Returns:
        - main groups or None: Retrieved prepared data entry or None if not found.
        """
        return self.session.query(PreparedData).filter_by(id=id).first()

    def get_all_prepared_data_entries(self):
        """
        Retrieves all prepared data  entries.

        Returns:
        - list: List of all prepared data  entries.
        """
        return self.session.query(PreparedData).all()

    def update_prepared_data(self, data):
        """
        Updates a prepared data entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated prepared data entry's id
        """
        updated_ids = []

        try:
            existing_record = self.get_prepared_data_by_id(data.get("id"))
            if existing_record:
                for id, value in data.items():
                    setattr(existing_record, id, value)

                self.session.commit()
                self.logger.info(f"Updated prepared data entry with id: {existing_record.id}")
                updated_ids.append(existing_record.id)
            else:
                self.save_prepared_data(data)

        except NoResultFound:
            updated_ids.append(self.save_prepared_data(data))

        return updated_ids

    def delete_prepared_data_by_id(self, id):
        """
        Deletes a prepared data entry by its id.

        Parameters:
        - code (str): prepared data entry id to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        prepared_data = self.session.query(PreparedData).filter_by(id=id).first()
        if prepared_data:
            self.session.delete(prepared_data)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the prepared_data table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(PreparedData.__tablename__)

    def create_table(self):
        """
        Create the tse_prepared_data table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                PreparedData.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False
