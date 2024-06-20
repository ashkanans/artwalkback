from sqlalchemy import inspect, desc
from sqlalchemy.ext.declarative import declarative_base

from backend.scraper.codal.model.letter import Letter
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class LetterDao(BaseLogger):
    def __init__(self, session):
        """
        Initializes the LetterDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        super().__init__()
        self.session = session

    def save_letter(self, data):
        """
        Saves a new letter.

        Parameters:
        - data (dict): Dictionary containing letter data.

        Returns:
        - Letter: Saved letter object.
        """
        letter = Letter(**data)
        self.session.add(letter)
        self.session.commit()
        self.logger.info(f"Saved letter with tracingNo: {letter.TracingNo}")
        return letter

    def get_all_letters(self):
        """
        Retrieves all letters.

        Returns:
        - list: List of all letters.
        """
        return self.session.query(Letter).all()

    def get_letter_by_tracing_no(self, tracing_no):
        """
        Retrieves a letter by its tracing number.

        Parameters:
        - tracing_no (int): Tracing number to retrieve.

        Returns:
        - Letter or None: Retrieved letter or None if not found.
        """
        return self.session.query(Letter).filter_by(TracingNo=tracing_no).first()

    def update_letter(self, data):
        """
        Updates a letter.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - Letter or None: Updated letter object or None if not found.
        """
        existing_record = self.session.query(Letter).filter_by(TracingNo=data.get("TracingNo")).first()
        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)
            self.session.commit()
            self.logger.info(f"Updated letter with tracingNo: {existing_record.TracingNo}")
            return existing_record.TracingNo
        else:
            return self.save_letter(data)

    def delete_letter(self, tracing_no):
        """
        Deletes a letter by its tracing number.

        Parameters:
        - tracing_no (int): Tracing number to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        letter = self.session.query(Letter).filter_by(TracingNo=tracing_no).first()
        if letter:
            self.session.delete(letter)
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
        return inspector.has_table(Letter.__tablename__)

    def create_table(self):
        """
        Create the letters table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                Letter.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.error(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_letter_by_symbol(self, symbol):
        """
                Retrieves letters by its symbol.

                Parameters:
                - symbol (str): Symbol to retrieve.

                Returns:
                - Letter or None: Retrieved letter or None if not found.
        """
        return self.session.query(Letter).filter_by(Symbol=symbol).all()

    def get_monthly_performance_letters_by_symbol(self, symbol):
        return self.session.query(Letter).filter_by(Symbol=symbol, LetterCode='ن-۳۰').all()

    def get_most_recent_letter_by_symbol(self, symbol):
        """
        Retrieves the most recent letter for a given symbol based on SentDateTime.

        Args:
        - session (Session): SQLAlchemy session object.
        - symbol (str): Symbol for which to retrieve the most recent letter.

        Returns:
        - Letter or None: Most recent letter object for the symbol, or None if not found.
        """
        return self.session.query(Letter).filter_by(Symbol=symbol).order_by(desc(Letter.SentDateTime)).first()
