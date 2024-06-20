from sqlalchemy import inspect, desc, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.codal.model.letters_map import LetterMAP
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class LettersMapDao(BaseLogger):
    def __init__(self, session: Session):
        """
        Initializes the LettersMapDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        super().__init__()
        self.session = session

    def save_letters_map(self, data):
        """
        Saves a new LetterMap entry.

        Parameters:
        - data (dict): Dictionary containing LetterMap data.

        Returns:
        - LetterMap: Saved LetterMap object.
        """
        letters_map = LetterMAP(**data)
        self.session.add(letters_map)
        self.session.commit()
        self.logger.info(f"LetterMap saved, annID: f{letters_map.annID}")
        return letters_map.annID

    def get_all_letters_maps(self):
        """
        Retrieves all LetterMap entries.

        Returns:
        - list: List of all LetterMap entries.
        """
        return self.session.query(LetterMAP).all()

    def get_letters_map_by_ann_id(self, ann_id):
        """
        Retrieves a LetterMap entry by its AnnID.

        Parameters:
        - ann_id (str): AnnID to retrieve.

        Returns:
        - LetterMap or None: Retrieved LetterMap or None if not found.
        """
        return self.session.query(LetterMAP).filter_by(annID=ann_id).first()

    def get_letters_map_by_one_month_period_until(self, one_month_period_until):
        """
        Retrieves a LetterMap entry by its One_Month_Period_Until.

        Parameters:
        - one_month_period_until (str): One_Month_Period_Until to retrieve.

        Returns:
        - LetterMap or None: Retrieved LetterMap or None if not found.
        """
        return self.session.query(LetterMAP).filter_by(periodEndToDate=one_month_period_until).first()

    def update_letters_map(self, data):
        """
        Updates a LetterMap entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - LetterMap or None: Updated LetterMap object or None if not found.
        """
        tracingData = data['tracingNo']
        existing_record = self.get_letters_map_by_tracingNo(tracingData)
        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)
            self.session.commit()
            self.logger.info(f"LetterMap updated, annID: f{existing_record.annID}")
            return existing_record.annID
        else:
            return self.save_letters_map(data)

    def delete_letters_map(self, ann_id):
        """
        Deletes a LetterMap entry by its AnnID.

        Parameters:
        - ann_id (str): AnnID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        letters_map = self.session.query(LetterMAP).filter_by(AnnID=ann_id).first()
        if letters_map:
            self.session.delete(letters_map)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(LetterMAP.__tablename__)

    def create_table(self):
        """
        Create the codal_letters_map table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                LetterMAP.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_letters_map_by_tracingNo(self, tracingNo):
        return self.session.query(LetterMAP).filter_by(tracingNo=tracingNo).first()

    def get_recent_letters_by_symbol(self, symbol):
        """
        Retrieves the 10 recent list of LetterMap entry based on publishDateTime

        Returns:
        - list of LetterMap or None: Retrieved LetterMap or None if not found.
        """
        return self.session.query(LetterMAP). \
            filter(LetterMAP.symbol == symbol). \
            filter(LetterMAP.type != 6). \
            filter(func.substring(LetterMAP.publishDateTime, 1, 4).cast(Integer) > 1399). \
            order_by(desc(LetterMAP.publishDateTime)).all()

    def get_income_statemenet_letters(self, symbol, title_text):
        """
                Retrieves the 10 recent list of LetterMap entry based on publishDateTime

                Returns:
                - list of LetterMap or None: Retrieved LetterMap or None if not found.
                """
        return self.session.query(LetterMAP).filter(LetterMAP.symbol == symbol). \
            filter(LetterMAP.publishDateTime != 'None'). \
            filter(func.substring(LetterMAP.publishDateTime, 1, 4).cast(Integer) > 1398). \
            filter(LetterMAP.reportName.like(f"%{title_text}%")). \
            order_by(desc(LetterMAP.publishDateTime)).all()
