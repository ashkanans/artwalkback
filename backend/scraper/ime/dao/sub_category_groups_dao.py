from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

from backend.scraper.ime.model.sub_category_groups import SubCategoryGroups
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class SubCategoryGroupsDao(BaseLogger):
    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the SubCategoryGroupsDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_sub_category_groups_info(self, data):
        """
        Saves a new sub category groups info entry.

        Parameters:
      - data (List of dict): list of Dictionary containing updated data.

        Returns:
        - int: Saved sub category groups info entry's ID
        """
        sub_category_groups_info = SubCategoryGroups(**data)
        self.session.add(sub_category_groups_info)
        self.session.commit()
        self.logger.info(f"Saved sub category groups info entry with ID: {sub_category_groups_info.name}")
        return sub_category_groups_info.code

    def get_all_sub_category_groups_info_entries(self):
        """
        Retrieves all sub category groups info entries.

        Returns:
        - list: List of all sub category groups info entries.
        """
        return self.session.query(SubCategoryGroups).all()

    def get_sub_category_groups_info_by_id(self, code):
        """
        Retrieves a  sub category groups info entry by its ID.

        Parameters:
        - code (str): sub category groups info entry ID to retrieve.

        Returns:
        - InstrumentInfo or None: Retrieved sub category groups info entry or None if not found.
        """
        return self.session.query(SubCategoryGroups).filter_by(code=code).first()

    def update_sub_category_groups_info(self, data):
        """
        Updates a sub category groups info entry.

        Parameters:
        - data (List of dict): list of Dictionary containing updated data.

        Returns:
        - str: Updated sub category groups info entry's ID
        """
        updated_ids = []
        for item in data:
            try:
                existing_record = self.get_sub_category_groups_info_by_id(item.get("code"))
                if existing_record:
                    for key, value in item.items():
                        setattr(existing_record, key, value)

                    self.session.commit()
                    self.logger.info(f"Updated sub category groups info entry with ID: {existing_record.name}")
                    updated_ids.append(existing_record.code)
                else:
                    self.save_sub_category_groups_info(item)

            except NoResultFound:
                updated_ids.append(self.save_sub_category_groups_info(item))

        return updated_ids

    def delete_sub_category_groups_info_by_id(self, code):
        """
        Deletes a sub category groups info entry by its ID.

        Parameters:
        - code (str): sub category groups info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        sub_category_groups = self.session.query(SubCategoryGroups).filter_by(code=code).first()
        if sub_category_groups:
            self.session.delete(sub_category_groups)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the sub_category_groups_info table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(SubCategoryGroups.__tablename__)

    def create_table(self):
        """
        Create the ime_sub_category_groups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                SubCategoryGroups.__table__.create(self.session.bind)
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
        code_values = self.session.query(SubCategoryGroups.code).all()
        return [value[0] for value in code_values]
