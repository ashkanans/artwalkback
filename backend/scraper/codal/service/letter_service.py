import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.codal.dao.letter_dao import LetterDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class LetterService:
    def __init__(self):
        """
        Initializes the LetterService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.letter_dao = LetterDao(session)

    def save_letter(self, data):
        """
        Saves a new letter.

        Parameters:
        - data (dict): Dictionary containing letter data.

        Returns:
        - Letter: Saved letter object.
        """
        return self.letter_dao.save_letter(data)

    def get_all_letters(self):
        """
        Retrieves all letters.

        Returns:
        - list: List of all letters.
        """
        return self.letter_dao.get_all_letters()

    def get_letter_by_tracing_no(self, tracing_no):
        """
        Retrieves a letter by its tracing number.

        Parameters:
        - tracing_no (int): Tracing number to retrieve.

        Returns:
        - Letter or None: Retrieved letter or None if not found.
        """
        return self.letter_dao.get_letter_by_tracing_no(tracing_no)

    def update_letter(self, data):
        """
        Updates a letter.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - Letter or None: Updated letter object or None if not found.
        """
        financialYearUntilMonth = self.extract_date(data.get("Title"))
        data["FinancialYearUntil"] = financialYearUntilMonth
        data = {key: str(value) for key, value in data.items()}
        return self.letter_dao.update_letter(data)

    def delete_letter(self, tracing_no):
        """
        Deletes a letter by its tracing number.

        Parameters:
        - tracing_no (int): Tracing number to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.letter_dao.delete_letter(tracing_no)

    def create_table(self):
        """
        Create the letters table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.letter_dao.create_table()

    def table_exists(self):
        """
        Create the main groups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """

        return self.letter_dao.table_exists()
    def extract_date(self, input_string):
        # Use regular expression to find the date pattern
        match = re.search(r'\b(\d{4}/\d{2}/\d{2})\b', input_string)

        if match:
            # Extract the matched date and return it
            return match.group(1)
        else:
            # Return None if no date is found in the input string
            return None

    def get_letter_by_symbol(self, symbol):
        return self.letter_dao.get_letter_by_symbol(symbol)

    def get_monthly_performance_letters_by_symbol(self, symbol):
        return self.letter_dao.get_monthly_performance_letters_by_symbol(symbol)

    def get_most_recent_letter_by_symbol(self, symbol):
        return self.letter_dao.get_most_recent_letter_by_symbol(symbol)
