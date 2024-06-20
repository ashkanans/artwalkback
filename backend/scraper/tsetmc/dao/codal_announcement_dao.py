import time

from sqlalchemy import inspect, Engine, desc
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.codal_announcement import CodalAnnouncement


class CodalAnnouncementDao(BaseLogger):
    def __init__(self, session: Session, engine: Engine, dynamic_tablename: str):
        super().__init__()
        """
        Initializes the CodalAnnouncementDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.engine = engine
        self.session = session
        self.dynamic_tablename = dynamic_tablename

        # Set the dynamic table name for ClosingPriceDailyList
        CodalAnnouncement.__table__.name = dynamic_tablename

    def save_codal_announcement(self, data):
        """
        Saves a new codal announcement entry.

        Parameters:
        - data (dict): Dictionary containing codal announcement data.

        Returns:
        - int: Saved codal announcement entry's ID
        """
        codal_instance = CodalAnnouncement(**data)
        self.session.add(codal_instance)
        self.session.commit()
        print(f"Codal announcement saved: {codal_instance.id}")
        return codal_instance.id

    def get_all_codal_announcement(self):
        """
        Retrieves all codal announcement entries.

        Returns:
        - list: List of all codal announcement entries.
        """
        return self.session.query(CodalAnnouncement).all()

    def get_recent_codal_announcements(self, num_announcements=5):
        """
        Retrieves the most recent codal announcement entries.

        Parameters:
        - num_announcements (int): Number of recent announcements to retrieve. Default is 10.

        Returns:
        - list: List of the most recent codal announcement entries.
        """
        return (
            self.session.query(CodalAnnouncement)
            .order_by(desc(CodalAnnouncement.publishDateTime_DEven))
            .limit(num_announcements)
            .all()
        )

    def get_codal_announcement_by_id(self, codal_announcement_id):
        """
        Retrieves a codal announcement entry by its ID.

        Parameters:
        - codal_announcement_id (int): ID of the codal announcement entry to retrieve.

        Returns:
        - CodalAnnouncement or None: Retrieved codal announcement entry or None if not found.
        """
        return self.session.query(CodalAnnouncement).filter_by(id=codal_announcement_id).first()

    def update_codal_announcement(self, data):
        """
        Updates a codal announcement entry.

        Parameters:
        - codal_announcement_id (int): ID of the codal announcement entry to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - int: Updated codal announcement entry's ID
        """
        codal_announcement_id = data.get('id')
        codal_announcement_filename = data.get('fileName')
        try:
            existing_record = (self.session.query(CodalAnnouncement).filter_by(id=codal_announcement_id,
                                                                               fileName=codal_announcement_filename)
                               .one())

            for key, value in data.items():
                setattr(existing_record, key, value)

            self.session.commit()
            return existing_record.id

        except NoResultFound:
            return self.save_codal_announcement(data)

    def delete_codal_announcement_by_id(self, codal_announcement_id):
        """
        Deletes a codal announcement entry by its ID.

        Parameters:
        - codal_announcement_id (int): ID of the codal announcement entry to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        codal_announcement_instance = self.session.query(CodalAnnouncement).filter_by(id=codal_announcement_id).first()
        if codal_announcement_instance:
            self.session.delete(codal_announcement_instance)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the codal_announcement_table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(self.dynamic_tablename)

    def create_table(self):
        """
        Create the desired table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                print("Creating table...")
                CodalAnnouncement.__table__.create(self.session.bind)
                print(f"Table created: {self.dynamic_tablename}")
                time.sleep(0.5)
                return True
            except Exception as e:
                print(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        print(f"Table {self.dynamic_tablename} already exists. ")
        return False
