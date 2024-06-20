from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.codal.dao.letters_map_dao import LettersMapDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class LettersMapService:
    def __init__(self):
        """
        Initializes the LettersMapService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.letters_map_dao = LettersMapDao(session)

    def save_letters_map(self, data):
        """
        Saves a new LettersMap entry.

        Parameters:
        - data (dict): Dictionary containing LettersMap data.

        Returns:
        - LettersMap: Saved LettersMap object.
        """
        return self.letters_map_dao.save_letters_map(data)

    def get_all_letters_maps(self):
        """
        Retrieves all LettersMap entries.

        Returns:
        - list: List of all LettersMap entries.
        """
        return self.letters_map_dao.get_all_letters_maps()

    def get_letters_map_by_ann_id(self, ann_id):
        """
        Retrieves a LettersMap entry by its AnnID.

        Parameters:
        - ann_id (str): AnnID to retrieve.

        Returns:
        - LettersMap or None: Retrieved LettersMap or None if not found.
        """
        return self.letters_map_dao.get_letters_map_by_ann_id(ann_id)

    def get_letters_map_by_one_month_period_until(self, one_month_period_until):
        """
        Retrieves a LettersMap entry by its One_Month_Period_Until.

        Parameters:
        - one_month_period_until (str): One_Month_Period_Until to retrieve.

        Returns:
        - LettersMap or None: Retrieved LettersMap or None if not found.
        """
        return self.letters_map_dao.get_letters_map_by_one_month_period_until(one_month_period_until)

    def update_letters_map(self, data):
        """
        Updates a LettersMap entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - LettersMap or None: Updated LettersMap object or None if not found.
        """
        data = {key: str(value) for key, value in data.items()}
        return self.letters_map_dao.update_letters_map(data)

    def delete_letters_map(self, ann_id):
        """
        Deletes a LettersMap entry by its AnnID.

        Parameters:
        - ann_id (str): AnnID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.letters_map_dao.delete_letters_map(ann_id)

    def create_table(self):
        """
        Create the letters_map table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.letters_map_dao.create_table()

    def get_recent_letters_by_symbol(self, symbol):
        """
        Retrieves a list of LettersMap entry ending this year

        Returns:
        - List of LettersMap or None: Retrieved list of LettersMap or None if not found.
        """
        return self.letters_map_dao.get_recent_letters_by_symbol(symbol)

    def get_income_statemenet_letters(self, symbol, title_text):
        return self.letters_map_dao.get_income_statemenet_letters(symbol, title_text)
