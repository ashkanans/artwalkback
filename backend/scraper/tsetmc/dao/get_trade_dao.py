from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.get_trade import GetTrade

Base = declarative_base()


class GetTradeDao(BaseLogger):

    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the GetTradeDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_get_trade(self, data):
        """
               Saves a new get trade entry.

               Parameters:
               - data (dict): Dictionary containing closing price daily list data.

               Returns:
               - datetime: Saved closing price daily list entry's datetime
               """
        get_trade = GetTrade(**data)
        self.session.add(get_trade)
        self.session.commit()
        self.logger.info(f"get trade entry saved: {get_trade.id}")
        return get_trade.id

    def get_get_trade_by_id(self, id):
        """
        Retrieves a get trade entry by its id.

        Parameters:
        - code (str): get trade entry id to retrieve.

        Returns:
        - main groups or None: Retrieved get trade entry or None if not found.
        """
        return self.session.query(GetTrade).filter_by(id=id).first()

    def get_all_get_trade_entries(self):
        """
        Retrieves all get trade  entries.

        Returns:
        - list: List of all get trade  entries.
        """
        return self.session.query(GetTrade).all()

    def update_get_trade(self, data):
        """
        Updates a get trade entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated get trade entry's id
        """
        updated_ids = []

        try:
            existing_record = self.get_get_trade_by_id(data.get("id"))
            if existing_record:
                for id, value in data.items():
                    setattr(existing_record, id, value)

                self.session.commit()
                self.logger.info(f"Updated get trade entry with id: {existing_record.id}")
                updated_ids.append(existing_record.id)
            else:
                self.save_get_trade(data)

        except NoResultFound:
            updated_ids.append(self.save_get_trade(data))

        return updated_ids

    def delete_get_trade_by_id(self, id):
        """
        Deletes a get trade entry by its id.

        Parameters:
        - code (str): get trade entry id to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        get_trade = self.session.query(GetTrade).filter_by(id=id).first()
        if get_trade:
            self.session.delete(get_trade)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the get_trade table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(GetTrade.__tablename__)

    def create_table(self):
        """
        Create the tse_get_trade table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                GetTrade.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False
