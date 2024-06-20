from sqlalchemy import inspect

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tgju.model.profiles_today import ProfilesToday


class ProfilesTodayDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        """
        Initializes the ProfilesTodayDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_profile_today(self, data):
        """
        Saves a new profile today entry.

        Parameters:
        - data (list): List containing profile today data.

        Returns:
        - ProfilesToday: Saved profile today object.
        """
        profile_today = ProfilesToday(data)
        self.session.add(profile_today)
        self.session.commit()
        self.logger.info(f"Saved profile today entry with Key: {profile_today.Key}")
        return profile_today

    def get_all_profile_todays(self):
        """
        Retrieves all profile today entries.

        Returns:
        - list: List of all profile today entries.
        """
        return self.session.query(ProfilesToday).all()

    def get_profile_today_by_key(self, key):
        """
        Retrieves a profile today entry by its Key.

        Parameters:
        - key (str): Key to retrieve.

        Returns:
        - ProfilesToday or None: Retrieved profile today entry or None if not found.
        """
        return self.session.query(ProfilesToday).filter_by(Key=key).first()

    def update_profile_today(self, data):
        """
        Updates a profile today entry.

        Parameters:
        - data (list): List containing updated data.

        Returns:
        - ProfilesToday or None: Updated profile today entry object or None if not found.
        """
        key = f"{data[0]} {data[1]} {data[3]}"
        existing_record = self.get_profile_today_by_key(key)

        if existing_record:
            existing_record.Symbol = data[0]
            existing_record.Date = data[1]
            existing_record.Price = data[2]
            existing_record.Time = data[3]
            existing_record.Change_Amount = data[4]
            existing_record.Percentage_Change = data[5]

            self.session.commit()
            self.logger.info(f"Updated profile today entry with Key: {existing_record.Key}")
            return existing_record.Key
        else:
            return self.save_profile_today(data)

    def delete_profile_today(self, key):
        """
        Deletes a profile today entry by its Key.

        Parameters:
        - key (str): Key to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        profile_today = self.session.query(ProfilesToday).filter_by(Key=key).first()
        if profile_today:
            self.session.delete(profile_today)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(ProfilesToday.__tablename__, schema='tgju')

    def create_table(self):
        """
        Create the profiles_today table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                ProfilesToday.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False
