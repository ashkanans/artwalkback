from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.instrument_group import InstrumentGroup

Base = declarative_base()


class InstrumentGroupDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        """
        Initializes the InstrumentGroupDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_instrument_group(self, element):
        """
        Saves a new instrument group to the database.

        Parameters:
        - element (dict): element data to update

        Returns:
        - int: Saved instrument group's ID
        """
        instrumentgroup = InstrumentGroup(**element)

        self.session.add(instrumentgroup)
        self.logger.info(f"Instrument group saved Id: {instrumentgroup.id}, Name: {instrumentgroup.name}.")
        self.session.commit()

        return instrumentgroup.id

    def get_all_instrument_groups(self):
        """
        Retrieves all instrument groups from the database.

        Returns:
        - list: List of all instrument groups
        """
        return self.session.query(InstrumentGroup).all()

    def get_instrument_group_by_group_id(self, groupId):
        """
        Retrieves an instrument group by its ID from the database.

        Parameters:
        - groupId (int): Group ID to retrieve

        Returns:
        - InstrumentGroup or None: Retrieved instrument group or None if not found
        """
        return self.session.query(InstrumentGroup).filter_by(id=groupId).first()

    def delete_group_by_group_id(self, groupId):
        """
        Deletes an instrument group by its ID from the database.

        Parameters:
        - groupId (int): Group ID to delete

        Returns:
        - bool: True if deletion successful, False otherwise
        """
        instrumentGroup = self.session.query(InstrumentGroup).filter_by(GroupId=groupId).first()
        if instrumentGroup:
            self.session.delete(instrumentGroup)
            self.session.commit()
            return True
        return False

    def update_instrument_group(self, element):
        """
        Updates an instrument group in the database.

        Parameters:
        - element (dict): element data to update

        Returns:
        - int: Updated instrument group's ID
        """

        existing_record = self.get_instrument_group_by_group_id(element.get('id'))
        if existing_record:
            for key, value in element.items():
                setattr(existing_record, key, value)
            self.session.commit()
            self.logger.info(
                f"Instrument group updated Id: {existing_record.id}, Name: {existing_record.name}.")
            return existing_record.id

        else:
            # If no record found, insert a new one
            return self.save_instrument_group(element)

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Parameters:
        - table_name (str): The name of the table to check.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(InstrumentGroup.__tablename__, schema='tsetmc')

    def create_table(self):
        """
        Create the instrumentgroups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                InstrumentGroup.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_instrument_group_by_group_code(self, sector_code):
        """
        Retrieves an instrument group by Group Code from the database.

        Parameters:
        - groupId (int): Group ID to retrieve

        Returns:
        - InstrumentGroup or None: Retrieved instrument group or None if not found
        """
        return self.session.query(InstrumentGroup).filter_by(GroupCode=sector_code).first()

    def get_all_instrument_codes(self):
        groups = self.session.query(InstrumentGroup).all()
        return [group.code for group in groups]
