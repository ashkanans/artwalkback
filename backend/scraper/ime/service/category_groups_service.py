from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.ime.dao.category_groups_dao import CategoryGroupsDao
from backend.scraper.logger.base_logger import BaseLogger

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class CategoryGroupsService(BaseLogger):
    def __init__(self):
        """
        Initializes the CategoryGroupsService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.category_groups_info_dao = CategoryGroupsDao(session)

    def save_category_groups_info(self, data):
        """
        Saves a new category groups info entry.

        Parameters:
        - data (list of dict): List of Dictionary containing updated data.

        Returns:
        - int: Saved category groups info entry's ID
        """
        return self.category_groups_info_dao.save_category_groups_info(data)

    def get_all_category_groups_info_entries(self):
        """
        Retrieves all category groups info entries.

        Returns:
        - list: List of all category groups info entries.
        """
        return self.category_groups_info_dao.get_all_category_groups_info_entries()

    def get_category_groups_info_by_id(self, code):
        """
        Retrieves a category groups info entry by its ID.

        Parameters:
        - code (str): category groups info entry ID to retrieve.

        Returns:
        - CategoryGroups or None: Retrieved category groups info entry or None if not found.
        """
        return self.category_groups_info_dao.get_category_groups_info_by_id(code)

    def update_category_groups_info(self, data):
        """
        Updates a category groups info entry.

        Parameters:
        - code (str): category groups info entry ID to update.
        - data (list of dict): List of Dictionary containing updated data.

        Returns:
        - str: Updated category groups info entry's ID
        """
        result = []
        for item in data:
            result.append({"name": item.get('name'), "code": item.get('code')})

        return self.category_groups_info_dao.update_category_groups_info(result)

    def delete_category_groups_info_by_id(self, code):
        """
        Deletes a category groups info entry by its ID.

        Parameters:
        - code (str): category groups info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.category_groups_info_dao.delete_category_groups_info_by_id(code)

    def create_table(self):
        """
        Create the category groups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.category_groups_info_dao.create_table()

    def get_all_ins_codes(self):
        """
        Retrieves all persian symbols.

        Returns:
        - list: List of all persian symbols.
        """
        return self.category_groups_info_dao.get_all_ins_codes()

    def table_exists(self):
        """
        Create the category groups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.category_groups_info_dao.table_exists()
