from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.msg_by_flow import MsgByFlow

Base = declarative_base()


class MsgByFlowDao(BaseLogger):

    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the MsgByFlowDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_msg_by_flow(self, data):
        """
               Saves a new msg by flow entry.

               Parameters:
               - data (dict): Dictionary containing closing price daily list data.

               Returns:
               - datetime: Saved closing price daily list entry's datetime
               """
        msg_by_flow = MsgByFlow(**data)
        self.session.add(msg_by_flow)
        self.session.commit()
        self.logger.info(f"msg by flows entry saved: {msg_by_flow.tseMsgIdn}")
        return msg_by_flow.tseMsgIdn

    def get_msg_by_flow_by_tseMsgIdn(self, tseMsgIdn):
        """
        Retrieves a msg by flows entry by its tseMsgIdn.

        Parameters:
        - code (str): msg by flows entry tseMsgIdn to retrieve.

        Returns:
        - main groups or None: Retrieved msg by flows entry or None if not found.
        """
        return self.session.query(MsgByFlow).filter_by(tseMsgIdn=tseMsgIdn).first()

    def get_all_msg_by_flow_entries(self):
        """
        Retrieves all msg by flows  entries.

        Returns:
        - list: List of all msg by flows  entries.
        """
        return self.session.query(MsgByFlow).all()

    def update_msg_by_flow(self, data):
        """
        Updates a msg by flows entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated msg by flows entry's tseMsgIdn
        """
        updated_ids = []

        try:
            existing_record = self.get_msg_by_flow_by_tseMsgIdn(data.get("tseMsgIdn"))
            if existing_record:
                for tseMsgIdn, value in data.items():
                    setattr(existing_record, tseMsgIdn, value)

                self.session.commit()
                self.logger.info(f"Updated msg by flows entry with tseMsgIdn: {existing_record.tseMsgIdn}")
                updated_ids.append(existing_record.tseMsgIdn)
            else:
                self.save_msg_by_flow(data)

        except NoResultFound:
            updated_ids.append(self.save_msg_by_flow(data))

        return updated_ids

    def delete_msg_by_flow_by_tseMsgIdn(self, tseMsgIdn):
        """
        Deletes a msg by flows entry by its tseMsgIdn.

        Parameters:
        - code (str): msg by flows entry tseMsgIdn to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        msg_by_flow = self.session.query(MsgByFlow).filter_by(tseMsgIdn=tseMsgIdn).first()
        if msg_by_flow:
            self.session.delete(msg_by_flow)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the msg_by_flow table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(MsgByFlow.__tablename__)

    def create_table(self):
        """
        Create the tse_msg_by_flow table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                MsgByFlow.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False
