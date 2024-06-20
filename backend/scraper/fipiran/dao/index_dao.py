from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

from backend.scraper.fipiran.model.index import Index
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class IndexDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        """
        Initializes the IndexDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_index(self, data):
        """
        Saves a new index to the database.

        Parameters:
        - name (str): Index name
        - value (str): Index value
        - dateissue (Date): Date of issue
        - gregorian_date (Date): Gregorian date
        - solar_date (Date): Solar date

        Returns:
        - int: Saved index's ID
        """
        index = Index(**data)

        self.session.add(index)
        self.logger.info(f"Record {index.instrumentID} saved for date: {index.gregorian_date}")
        self.session.commit()

        return index.id

    def get_all_indices(self):
        """
        Retrieves all indices from the database.

        Returns:
        - list: List of all indices
        """
        return self.session.query(Index).all()

    def get_index_by_id(self, index_id):
        """
        Retrieves an index by its ID from the database.

        Parameters:
        - index_id (int): Index ID to retrieve

        Returns:
        - Index or None: Retrieved index or None if not found
        """
        return self.session.query(Index).filter_by(id=index_id).first()

    def delete_index_by_id(self, index_id):
        """
        Deletes an index by its ID from the database.

        Parameters:
        - index_id (int): Index ID to delete

        Returns:
        - bool: True if deletion successful, False otherwise
        """
        index = self.session.query(Index).filter_by(id=index_id).first()
        if index:
            self.session.delete(index)
            self.session.commit()
            return True
        return False

    def update_index(self, data):
        """
        Updates an index in the database.

        Parameters:
        - index_id (int): Index ID to update
        - name (str): New index name
        - value (str): New index value
        - dateissue (Date): New date of issue
        - gregorian_date (Date): New Gregorian date
        - solar_date (Date): New Solar date

        Returns:
        - int: Updated index's ID
        """

        existing_record = self.get_by_instrumentId_and_dateissue(data.get('instrumentID'), data.get('dateissue'))
        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)

            # Commit the changes
            self.session.commit()
            self.logger.info(
                f"Record {existing_record.instrumentID} updated for date: {existing_record.gregorian_date}")
            return existing_record.instrumentID

        else:
            # If no record found, insert a new one
            return self.save_index(data)

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(Index.__tablename__)

    def create_table(self):
        """
        Create the index table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                Index.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_by_instrumentId_and_dateissue(self, instrumentID, dateissue):
        return self.session.query(Index).filter_by(instrumentID=instrumentID, dateissue=dateissue).first()

    def get_by_nameFa(self, nameFa):
        return self.session.query(Index).filter(Index.nameFa.like(f"%{nameFa}%")).all()

    def get_index_by_sectorCode(self, sector_code):
        return self.session.query(Index).filter_by(intId=sector_code).all()
