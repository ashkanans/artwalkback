from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.best_limits import BestLimits

Base = declarative_base()


class BestLimitsDao(BaseLogger):

    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the BestLimitsDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_best_limits(self, data):
        """
               Saves a new best limit entry.

               Parameters:
               - data (dict): Dictionary containing closing price daily list data.

               Returns:
               - datetime: Saved closing price daily list entry's datetime
               """
        best_limits = BestLimits(**data)
        self.session.add(best_limits)
        self.session.commit()
        self.logger.info(f"Best Limits entry saved: {best_limits.key}")
        return best_limits.key

    def get_best_limits_by_key(self, key):
        """
        Retrieves a best limits entry by its key.

        Parameters:
        - code (str): best limits entry key to retrieve.

        Returns:
        - main groups or None: Retrieved best limits entry or None if not found.
        """
        return self.session.query(BestLimits).filter_by(key=key).first()

    def get_all_best_limits_entries(self):
        """
        Retrieves all best limits  entries.

        Returns:
        - list: List of all best limits  entries.
        """
        return self.session.query(BestLimits).all()

    def update_best_limits(self, data):
        """
        Updates a best limits entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated best limits entry's key
        """
        updated_ids = []

        try:
            existing_record = self.get_best_limits_by_key(data.get("key"))
            if existing_record:
                for key, value in data.items():
                    setattr(existing_record, key, value)

                self.session.commit()
                self.logger.info(f"Updated best limits entry with key: {existing_record.key}")
                updated_ids.append(existing_record.key)
            else:
                self.save_best_limits(data)

        except NoResultFound:
            updated_ids.append(self.save_best_limits(data))

        return updated_ids

    def delete_best_limits_by_key(self, key):
        """
        Deletes a best limits entry by its key.

        Parameters:
        - code (str): best limits entry key to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        best_limits = self.session.query(BestLimits).filter_by(key=key).first()
        if best_limits:
            self.session.delete(best_limits)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the best_limits table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(BestLimits.__tablename__)

    def create_table(self):
        """
        Create the tse_best_limits table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                BestLimits.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_row_data(self, inscode, number):
        key = inscode + " + " + str(number)
        return self.get_best_limits_by_key(key)

    def get_list_data(self, inscode):

        lst_sell_volume = []
        lst_sell = []
        lst_buy_volume = []
        lst_buy = []

        for i in range(1, 6):
            data = self.get_row_data(inscode, i)
            if data != None:
                lst_buy_volume.append(data.qTitMeDem)
                lst_buy.append(data.pMeDem)
                lst_sell_volume.append(data.qTitMeOf)
                lst_sell.append(data.pMeOf)
            else:
                lst_buy_volume.append(data)
                lst_buy.append(data)
                lst_sell_volume.append(data)
                lst_sell.append(data)

        combined_list = lst_buy_volume + lst_buy + lst_sell + lst_sell_volume
        return combined_list
