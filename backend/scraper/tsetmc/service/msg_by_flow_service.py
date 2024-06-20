from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.dao.msg_by_flow_dao import MsgByFlowDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class MsgByFlowService(BaseLogger):
    def __init__(self):
        """
        Initializes the MsgByFlowService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.msg_by_flow_dao = MsgByFlowDao(session)

    def save_msg_by_flow(self, data):
        """
        Saves a new msg by flow  entry.

        Parameters:
        - data (dict): Dictionary containing msg by flow  data.

        Returns:
        - int: Saved msg by flow  entry's tseMsgIdn
        """
        return self.msg_by_flow_dao.save_msg_by_flow(data)

    def get_all_msg_by_flow_entries(self):
        """
        Retrieves all msg by flow  entries.

        Returns:
        - list: List of all msg by flow  entries.
        """
        return self.msg_by_flow_dao.get_all_msg_by_flow_entries()

    def get_msg_by_flow_by_tseMsgIdn(self, code):
        """
        Retrieves a msg by flow  entry by its tseMsgIdn.

        Parameters:
        - code (str): msg by flow  entry tseMsgIdn to retrieve.

        Returns:
        - MsgByFlow or None: Retrieved msg by flow  entry or None if not found.
        """
        return self.msg_by_flow_dao.get_msg_by_flow_by_tseMsgIdn(code)

    def update_msg_by_flow(self, data):
        """
        Updates a msg by flow  entry.

        Parameters:
        - code (str): msg by flow  entry tseMsgIdn to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated msg by flow  entry's tseMsgIdn
        """

        return self.msg_by_flow_dao.update_msg_by_flow(data)

    def delete_msg_by_flow_by_tseMsgIdn(self, code):
        """
        Deletes a msg by flow  entry by its tseMsgIdn.

        Parameters:
        - code (str): msg by flow  entry tseMsgIdn to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.msg_by_flow_dao.delete_msg_by_flow_by_tseMsgIdn(code)

    def create_table(self):
        """
        Create the msg by flow table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.msg_by_flow_dao.create_table()

    def table_exists(self):
        """
        Create the msg by flow table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """

        return self.msg_by_flow_dao.table_exists()
