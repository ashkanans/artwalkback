from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.tradingeconomics.dao.profiles_history_dao import ProfilesHistoryDao

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class ProfilesHistoryService:
    def __init__(self):
        """
        Initializes the ProfilesHistoryService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.profiles_history_dao = ProfilesHistoryDao(session)

    def save_profiles_history(self, data):
        """
        Saves a new ProfilesHistory entry.

        Parameters:
        - data (dict): Dictionary containing ProfilesHistory data.

        Returns:
        - ProfilesHistory: Saved ProfilesHistory object.
        """
        return self.profiles_history_dao.save_profiles_history(data)

    def get_all_profiles_histories(self):
        """
        Retrieves all ProfilesHistory entries.

        Returns:
        - list: List of all ProfilesHistory entries.
        """
        return self.profiles_history_dao.get_all_profiles_histories()

    def get_profiles_history_by_ann_id(self, ann_id):
        """
        Retrieves a ProfilesHistory entry by its AnnID.

        Parameters:
        - ann_id (str): AnnID to retrieve.

        Returns:
        - ProfilesHistory or None: Retrieved ProfilesHistory or None if not found.
        """
        return self.profiles_history_dao.get_profiles_history_by_ann_id(ann_id)

    def get_profiles_history_by_one_month_period_until(self, one_month_period_until):
        """
        Retrieves a ProfilesHistory entry by its One_Month_Period_Until.

        Parameters:
        - one_month_period_until (str): One_Month_Period_Until to retrieve.

        Returns:
        - ProfilesHistory or None: Retrieved ProfilesHistory or None if not found.
        """
        return self.profiles_history_dao.get_profiles_history_by_one_month_period_until(one_month_period_until)

    def update_profiles_history(self, data):
        """
        Updates a ProfilesHistory entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - ProfilesHistory or None: Updated ProfilesHistory object or None if not found.
        """
        updated_items = []
        for item in data:
            updated_year = self.profiles_history_dao.update_profiles_history(item)
            updated_items.append(updated_year)

        return updated_items
        # return self.profiles_history_dao.update_profiles_history(data)

    def delete_profiles_history(self, ann_id):
        """
        Deletes a ProfilesHistory entry by its AnnID.

        Parameters:
        - ann_id (str): AnnID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.profiles_history_dao.delete_profiles_history(ann_id)

    def create_table(self):
        """
        Create the profiles_history table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.profiles_history_dao.create_table()

    def get_first_price_by_AnnId_and_year(self, annId, year):
        return self.profiles_history_dao.get_first_price_by_AnnId_and_year(annId, year)

    def get_last_price_by_AnnId(self, annId):
        return self.profiles_history_dao.get_last_price_by_AnnId(annId)
