from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.ime.dao.sub_category_groups_dao import SubCategoryGroupsDao
from backend.scraper.logger.base_logger import BaseLogger

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class SubCategoryGroupsService(BaseLogger):
    def __init__(self):
        """
        Initializes the SubCategoryGroupsService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.sub_category_groups_info_dao = SubCategoryGroupsDao(session)

    def save_sub_category_groups_info(self, data):
        """
        Saves a new sub category groups info entry.

        Parameters:
        - data (list of dict): List of Dictionary containing updated data.

        Returns:
        - int: Saved sub category groups info entry's ID
        """
        return self.sub_category_groups_info_dao.save_sub_category_groups_info(data)

    def get_all_sub_category_groups_info_entries(self):
        """
        Retrieves all sub category groups info entries.

        Returns:
        - list: List of all sub category groups info entries.
        """
        return self.sub_category_groups_info_dao.get_all_sub_category_groups_info_entries()

    def get_sub_category_groups_info_by_id(self, code):
        """
        Retrieves a sub category groups info entry by its ID.

        Parameters:
        - code (str): sub category groups info entry ID to retrieve.

        Returns:
        - SubCategoryGroups or None: Retrieved sub category groups info entry or None if not found.
        """
        return self.sub_category_groups_info_dao.get_sub_category_groups_info_by_id(code)

    def update_sub_category_groups_info(self, data):
        """
        Updates a sub category groups info entry.

        Parameters:
        - code (str): sub category groups info entry ID to update.
        - data (list of dict): List of Dictionary containing updated data.

        Returns:
        - str: Updated sub category groups info entry's ID
        """
        result = []
        for item in data:
            result.append({"name": item.get('name'), "code": item.get('code')})

        return self.sub_category_groups_info_dao.update_sub_category_groups_info(data)

    def delete_sub_category_groups_info_by_id(self, code):
        """
        Deletes a sub category groups info entry by its ID.

        Parameters:
        - code (str): sub category groups info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.sub_category_groups_info_dao.delete_sub_category_groups_info_by_id(code)

    def create_table(self):
        """
        Create the sub category groups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.sub_category_groups_info_dao.create_table()

    def get_all_ins_codes(self):
        """
        Retrieves all persian symbols.

        Returns:
        - list: List of all persian symbols.
        """
        return self.sub_category_groups_info_dao.get_all_ins_codes()

    def table_exists(self):
        """
        Create the sub category groups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.sub_category_groups_info_dao.table_exists()
