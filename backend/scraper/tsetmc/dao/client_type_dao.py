from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.client_type import ClientType

Base = declarative_base()


class ClientTypeDao(BaseLogger):

    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the ClientTypeDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_client_type(self, data):
        """
               Saves a new client type entry.

               Parameters:
               - data (dict): Dictionary containing closing price daily list data.

               Returns:
               - datetime: Saved closing price daily list entry's datetime
               """
        client_type = ClientType(**data)
        self.session.add(client_type)
        self.session.commit()
        self.logger.info(f"client types entry saved: {client_type.insCode}")
        return client_type.insCode

    def get_client_type_by_inscode(self, inscode):
        """
        Retrieves a client types entry by its inscode.

        Parameters:
        - code (str): client types entry inscode to retrieve.

        Returns:
        - main groups or None: Retrieved client types entry or None if not found.
        """
        return self.session.query(ClientType).filter_by(insCode=inscode).first()

    def get_all_client_type_entries(self):
        """
        Retrieves all client types  entries.

        Returns:
        - list: List of all client types  entries.
        """
        return self.session.query(ClientType).all()

    def update_client_type(self, data):
        """
        Updates a client types entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated client types entry's inscode
        """
        updated_ids = []

        try:
            existing_record = self.get_client_type_by_inscode(data.get("insCode"))
            if existing_record:
                for inscode, value in data.items():
                    setattr(existing_record, inscode, value)

                self.session.commit()
                self.logger.info(f"Updated client types entry with inscode: {existing_record.insCode}")
                updated_ids.append(existing_record.insCode)
            else:
                self.save_client_type(data)

        except NoResultFound:
            updated_ids.append(self.save_client_type(data))

        return updated_ids

    def delete_client_type_by_inscode(self, inscode):
        """
        Deletes a client types entry by its inscode.

        Parameters:
        - code (str): client types entry inscode to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        client_type = self.session.query(ClientType).filter_by(inscode=inscode).first()
        if client_type:
            self.session.delete(client_type)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the client_type table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(ClientType.__tablename__)

    def create_table(self):
        """
        Create the tse_client_type table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                ClientType.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_list_data(self, inscode):

        result = []
        data = self.get_client_type_by_inscode(inscode)
        if data:
            result.append(data.buy_I_Volume)
            result.append(data.sell_I_Volume)
            result.append(data.buy_N_Volume)
            result.append(data.sell_N_Volume)
            result.append(data.buy_CountI)
            result.append(data.sell_CountI)
            result.append(data.buy_CountN)
            result.append(data.sell_CountN)
        else:
            result.append(None)
            result.append(None)
            result.append(None)
            result.append(None)
            result.append(None)
            result.append(None)
            result.append(None)
            result.append(None)

        return result
