from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

from backend.scraper.ime.model.category_groups import CategoryGroups
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class CategoryGroupsDao(BaseLogger):
    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the CategoryGroupsDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_category_groups_info(self, data):
        """
        Saves a new category groups info entry.

        Parameters:
        - data (List of dict): list of Dictionary containing updated data.

        Returns:
        - int: Saved category groups info entry's ID
        """
        category_groups_info = CategoryGroups(**data)
        self.session.add(category_groups_info)
        self.session.commit()
        self.logger.info(f"Saved category groups info entry with ID: {category_groups_info.name}")
        return category_groups_info.code

    def get_all_category_groups_info_entries(self):
        """
        Retrieves all category groups info entries.

        Returns:
        - list: List of all category groups info entries.
        """
        return self.session.query(CategoryGroups).all()

    def get_category_groups_info_by_id(self, code):
        """
        Retrieves a category groups info entry by its ID.

        Parameters:
        - code (str): category groups info entry ID to retrieve.

        Returns:
        - CategoryGroups or None: Retrieved category groups info entry or None if not found.
        """
        return self.session.query(CategoryGroups).filter_by(code=code).first()

    def update_category_groups_info(self, data):
        """
        Updates a category groups info entry.

        Parameters:
        - data (List of dict): list of Dictionary containing updated data.

        Returns:
        - str: Updated category groups info entry's ID
        """
        updated_ids = []
        for item in data:
            try:
                existing_record = self.get_category_groups_info_by_id(item.get("code"))
                if existing_record:
                    for key, value in item.items():
                        setattr(existing_record, key, value)

                    self.session.commit()
                    self.logger.info(f"Updated category groups info entry with ID: {existing_record.name}")
                    updated_ids.append(existing_record.code)
                else:
                    self.save_category_groups_info(item)

            except NoResultFound:
                updated_ids.append(self.save_category_groups_info(item))

        return updated_ids

    def delete_category_groups_info_by_id(self, code):
        """
        Deletes a category groups info entry by its ID.

        Parameters:
        - code (str): category groups info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        category_groups_info = self.session.query(CategoryGroups).filter_by(code=code).first()
        if category_groups_info:
            self.session.delete(category_groups_info)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the category_groups_info table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(CategoryGroups.__tablename__)

    def create_table(self):
        """
        Create the ime_category_groups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                CategoryGroups.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_all_ins_codes(self):
        """
        Retrieves all values in the code column.

        Parameters:
        - session: SQLAlchemy session object

        Returns:
        - list: List of all values in the code column.
        """
        code_values = self.session.query(CategoryGroups.code).all()
        return [value[0] for value in code_values]
