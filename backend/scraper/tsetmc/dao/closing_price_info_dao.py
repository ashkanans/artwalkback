from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.closing_price_info import ClosingPriceInfo

Base = declarative_base()


class ClosingPriceInfoDao(BaseLogger):

    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the ClosingPriceInfoDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_closing_price_info(self, data):
        """
               Saves a new closing price info entry.

               Parameters:
               - data (dict): Dictionary containing closing price daily list data.

               Returns:
               - datetime: Saved closing price daily list entry's datetime
               """
        closing_price_info = ClosingPriceInfo(**data)
        self.session.add(closing_price_info)
        self.session.commit()
        self.logger.info(f"closing price infos entry saved: {closing_price_info.insCode}")
        return closing_price_info.insCode

    def get_closing_price_info_by_inscode(self, inscode):
        """
        Retrieves a closing price infos entry by its inscode.

        Parameters:
        - code (str): closing price infos entry inscode to retrieve.

        Returns:
        - main groups or None: Retrieved closing price infos entry or None if not found.
        """
        return self.session.query(ClosingPriceInfo).filter_by(insCode=inscode).first()

    def get_all_closing_price_info_entries(self):
        """
        Retrieves all closing price infos  entries.

        Returns:
        - list: List of all closing price infos  entries.
        """
        return self.session.query(ClosingPriceInfo).all()

    def update_closing_price_info(self, data):
        """
        Updates a closing price infos entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated closing price infos entry's inscode
        """
        updated_ids = []

        try:
            existing_record = self.get_closing_price_info_by_inscode(data.get("insCode"))
            if existing_record:
                for inscode, value in data.items():
                    setattr(existing_record, inscode, value)

                self.session.commit()
                self.logger.info(f"Updated closing price infos entry with inscode: {existing_record.insCode}")
                updated_ids.append(existing_record.insCode)
            else:
                self.save_closing_price_info(data)

        except NoResultFound:
            updated_ids.append(self.save_closing_price_info(data))

        return updated_ids

    def delete_closing_price_info_by_inscode(self, inscode):
        """
        Deletes a closing price infos entry by its inscode.

        Parameters:
        - code (str): closing price infos entry inscode to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        closing_price_info = self.session.query(ClosingPriceInfo).filter_by(inscode=inscode).first()
        if closing_price_info:
            self.session.delete(closing_price_info)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the closing_price_info table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(ClosingPriceInfo.__tablename__)

    def create_table(self):
        """
        Create the tse_closing_price_info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                ClosingPriceInfo.__table__.create(self.session.bind)
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
        data = self.get_closing_price_info_by_inscode(inscode)

        if data:
            result.append(data.pDrCotVal)
            value5 = str(
                round((float(data.pDrCotVal) - float(data.priceYesterday)) / float(data.priceYesterday) * 100, 2))
            result.append(value5)  # 5 ???
            result.append(data.priceFirst)
            result.append(data.pClosing)
            percent = (float(data.pClosing) - float(data.priceYesterday)) / float(data.priceYesterday) * 100
            result.append(str(percent))
            result.append(data.priceYesterday)
            result.append(data.qTotTran5J)
            result.append(data.qTotCap)
            result.append(None)  # 12 ???
            result.append(data.priceMax)
            result.append(data.priceMin)
        else:
            result.append(None)
            result.append(None)
            result.append(None)
            result.append(None)
            result.append(None)
            result.append(None)
            result.append(None)
            result.append(None)
            result.append(None)
            result.append(None)
            result.append(None)

        return result
