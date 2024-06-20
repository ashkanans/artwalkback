from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

from backend.scraper.ime.model.main_groups import MainGroups
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class MainGroupsDao(BaseLogger):
    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the MainGroupsDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_main_groups_info(self, data):
        """
        Saves a new main groups info entry.

        Parameters:
        - data (dict): Dictionary containing main groups info data.

        Returns:
        - int: Saved main groups info entry's ID
        """
        main_groups_info = MainGroups(**data)
        self.session.add(main_groups_info)
        self.session.commit()
        self.logger.info(f"Saved main groups info entry with ID: {main_groups_info.Name}")
        return main_groups_info.code

    def get_all_main_groups_info_entries(self):
        """
        Retrieves all main groups info entries.

        Returns:
        - list: List of all main groups info entries.
        """
        return self.session.query(MainGroups).all()

    def get_main_groups_info_by_id(self, code):
        """
        Retrieves a main groups info entry by its ID.

        Parameters:
        - code (str): main groups info entry ID to retrieve.

        Returns:
        - main groups or None: Retrieved main groups info entry or None if not found.
        """
        return self.session.query(MainGroups).filter_by(code=code).first()

    def update_main_groups_info(self, data):
        """
        Updates a main groups info entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - str: Updated main groups info entry's ID
        """
        updated_ids = []
        for item in data:
            try:
                existing_record = self.get_main_groups_info_by_id(item.get("code"))
                if existing_record:
                    for key, value in item.items():
                        setattr(existing_record, key, value)

                    self.session.commit()
                    self.logger.info(f"Updated main groups info entry with ID: {existing_record.Name}")
                    updated_ids.append(existing_record.code)
                else:
                    self.save_main_groups_info(item)

            except NoResultFound:
                updated_ids.append(self.save_main_groups_info(item))

        return updated_ids

    def delete_main_groups_info_by_id(self, code):
        """
        Deletes a main groups info entry by its ID.

        Parameters:
        - code (str): main groups info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        main_groups_info = self.session.query(MainGroups).filter_by(code=code).first()
        if main_groups_info:
            self.session.delete(main_groups_info)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the main_groups_info table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(MainGroups.__tablename__)

    def create_table(self):
        """
        Create the ime_main_groups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                MainGroups.__table__.create(self.session.bind)
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
        Retrieves all values in the name column.

        Parameters:
        - session: SQLAlchemy session object

        Returns:
        - list: List of all values in the name column.
        """
        name_values = self.session.query(MainGroups.code).all()
        return [value[0] for value in name_values]
