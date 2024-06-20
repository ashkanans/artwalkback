from sqlalchemy import inspect
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

from backend.scraper.ime.model.producer_groups import ProducerGroups
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class ProducerGroupsDao(BaseLogger):
    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the ProducerGroupsDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_producer_groups_info(self, data):
        """
        Saves a new producer groups info entry.

        Parameters:
        - data (List of dict): list of Dictionary containing producer groups info data.

        Returns:
        - int: Saved Producer groups info entry's ID
        """
        producer_groups_info = ProducerGroups(**data)
        self.session.add(producer_groups_info)
        self.session.commit()
        self.logger.info(f"Saved producer groups info entry with ID: {producer_groups_info.name}")
        return producer_groups_info.code

    def get_all_producer_groups_info_entries(self):
        """
        Retrieves all producer groups info entries.

        Returns:
        - list: List of all producer groups info entries.
        """
        return self.session.query(ProducerGroups).all()

    def get_producer_groups_info_by_id(self, code):
        """
        Retrieves a producer groups info entry by its ID.

        Parameters:
        - code (str): Producer groups info entry ID to retrieve.

        Returns:
        - producer groups or None: Retrieved Producer groups info entry or None if not found.
        """
        return self.session.query(ProducerGroups).filter_by(code=code).first()

    def update_producer_groups_info(self, data):
        """
        Updates a producer groups info entry.

        Parameters:
        - data (List of dict): list of Dictionary containing updated data.

        Returns:
        - str: Updated producer groups info entry's ID
        """
        updated_ids = []
        for item in data:
            try:
                existing_record = self.get_producer_groups_info_by_id(item.get("code"))
                if existing_record:
                    for key, value in item.items():
                        setattr(existing_record, key, value)

                    self.session.commit()
                    self.logger.info(f"Updated producer groups info entry with ID: {existing_record.name}")
                    updated_ids.append(existing_record.code)
                else:
                    self.save_producer_groups_info(item)

            except NoResultFound:
                updated_ids.append(self.save_producer_groups_info(item))

        return updated_ids

    def delete_producer_groups_info_by_id(self, code):
        """
        Deletes a producer groups info entry by its ID.

        Parameters:
        - code (str): producer groups info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        producer_groups = self.session.query(ProducerGroups).filter_by(code=code).first()
        if producer_groups:
            self.session.delete(producer_groups)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the producer_groups_info table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(ProducerGroups.__tablename__)

    def create_table(self):
        """
        Create the ime_producer_groups table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                ProducerGroups.__table__.create(self.session.bind)
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
        code_values = self.session.query(ProducerGroups.code).all()
        return [value[0] for value in code_values]


