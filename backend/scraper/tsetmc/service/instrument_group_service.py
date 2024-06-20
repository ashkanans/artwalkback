from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.instument_group_dao import InstrumentGroupDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class InstrumentGroupService(BaseLogger):
    def __init__(self):
        """
        Initializes the InstrumentGroupService.

        Parameters:
        - session: SQLAlchemy session object
        """
        super().__init__()
        self.instrument_group_dao = InstrumentGroupDao(session)

    def save_instrument_group(self, GroupId, GroupCode, GroupType, GroupName, GroupDescription):
        """
        Saves a new instrument group.

        Parameters:
        - GroupId (int): Group ID
        - GroupCode (int): Group code
        - GroupType (str): Group type
        - GroupName (str): Group name
        - GroupDescription (str): Group description

        Returns:
        - int: Saved instrument group's ID
        """
        return self.instrument_group_dao.save_instrument_group(
            GroupId=GroupId,
            GroupCode=GroupCode,
            GroupType=GroupType,
            GroupName=GroupName,
            GroupDescription=GroupDescription
        )

    def get_all_instrument_groups(self):
        """
        Retrieves all instrument groups.

        Returns:
        - list: List of all instrument groups
        """
        return self.instrument_group_dao.get_all_instrument_groups()

    def get_instrument_group_by_group_id(self, groupId):
        """
        Retrieves an instrument group by its ID.

        Parameters:
        - groupId (int): Group ID to retrieve

        Returns:
        - InstrumentGroup or None: Retrieved instrument group or None if not found
        """
        return self.instrument_group_dao.get_instrument_group_by_group_id(groupId)

    def delete_group_by_group_id(self, groupId):
        """
        Deletes an instrument group by its ID.

        Parameters:
        - groupId (int): Group ID to delete

        Returns:
        - bool: True if deletion successful, False otherwise
        """
        return self.instrument_group_dao.delete_group_by_group_id(groupId)

    def update_instrument_group(self, element):
        """
        Updates an instrument group.

        Parameters:
        - element (dict): element data to update

        Returns:
        - int: Updated instrument group's ID
        """
        return self.instrument_group_dao.update_instrument_group(element)

    def create_table(self):
        """
        Create the instrumentgroups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.instrument_group_dao.create_table()

    def table_exists(self):
        """
        Create the instrumentgroups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.instrument_group_dao.table_exists()

    def get_instrument_group_by_group_code(self, sector_code):
        """
        Retrieves an instrument group by group code.

        Parameters:
        - groupId (int): sector_code to retrieve

        Returns:
        - InstrumentGroup or None: Retrieved instrument group or None if not found
        """
        return self.instrument_group_dao.get_instrument_group_by_group_code(sector_code)

    def get_all_instrument_codes(self):
        return self.instrument_group_dao.get_all_instrument_codes()
