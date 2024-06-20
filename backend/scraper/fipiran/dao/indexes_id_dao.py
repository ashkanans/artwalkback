from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

from backend.scraper.fipiran.model.indexes_id import IndexesId
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class IndexesIdDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        """
        Initializes the IndexesIdDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_indexes_id(self, data):
        """
        Saves a new index id to the database.

        Parameters:
        - InstrumentID (str): Index id
        - LVal30 (str): Index Name


        Returns:
        - int: Saved index's ID
        """
        index_id = IndexesId(**data)

        self.session.add(index_id)
        self.logger.info(f"Record {index_id.LVal30} saved with {index_id.InstrumentID} InstrumentID")
        self.session.commit()

        return index_id.InstrumentID

    def get_all_indexes_id(self):
        """
        Retrieves all indices id from the database.

        Returns:
        - list: List of all indices id
        """
        return self.session.query(IndexesId).all()

    def get_indexes_id_by_key(self, index_id):
        """
        Retrieves an index id by its InstrumentID from the database.

        Parameters:
        - index_id (int): Index ID to retrieve

        Returns:
        - Index or None: Retrieved index or None if not found
        """
        return self.session.query(IndexesId).filter_by(InstrumentID=index_id).first()

    def delete_indexes_id_by_key(self, index_id):
        """
        Deletes an index id by its InstrumentID from the database.

        Parameters:
        - index_id (int): Index ID to delete

        Returns:
        - bool: True if deletion successful, False otherwise
        """
        index_id = self.session.query(IndexesId).filter_by(InstrumentID=index_id).first()
        if index_id:
            self.session.delete(index_id)
            self.session.commit()
            return True
        return False

    def update_indexes_id(self, data):
        """
        Updates an index in the database.

         Parameters:
        - InstrumentID (str): Index id
        - LVal30 (str): Index Name

        Returns:
        - int: Updated index InstrumentID
        """

        existing_record = self.get_by_InstrumentID(data.get('InstrumentID'))
        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)

            # Commit the changes
            self.session.commit()
            self.logger.info(f"Record {existing_record.LVal30} updated with {existing_record.InstrumentID} InstrumentID")
            return existing_record.InstrumentID

        else:
            # If no record found, insert a new one
            return self.save_indexes_id(data)

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(IndexesId.__tablename__)

    def create_table(self):
        """
        Create the index table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                IndexesId.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_by_InstrumentID(self, index_id):
        return self.session.query(IndexesId).filter_by(InstrumentID=index_id,).first()