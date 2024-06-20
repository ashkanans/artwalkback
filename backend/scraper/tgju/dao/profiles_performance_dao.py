from sqlalchemy import inspect

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tgju.model.profiles_performance import ProfilesPerformance


class ProfilesPerformanceDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        """
        Initializes the ProfilesPerformanceDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_performance_profile(self, data):
        """
        Saves a new performance profile.

        Parameters:
        - data (dict): Dictionary containing performance profile data.

        Returns:
        - ProfilesPerformance: Saved performance profile object.
        """
        performance_profile = ProfilesPerformance(data)
        self.session.add(performance_profile)
        self.session.commit()
        self.logger.info(f"Saved performance profile entry with Symbol: {performance_profile.Symbol}")
        return performance_profile

    def get_all_performance_profiles(self):
        """
        Retrieves all performance profiles.

        Returns:
        - list: List of all performance profiles.
        """
        return self.session.query(ProfilesPerformance).all()

    def get_performance_profile_by_symbol(self, symbol):
        """
        Retrieves a performance profile by its Symbol.

        Parameters:
        - symbol (str): Symbol to retrieve.

        Returns:
        - ProfilesPerformance or None: Retrieved performance profile or None if not found.
        """
        return self.session.query(ProfilesPerformance).filter_by(Symbol=symbol).first()

    def update_performance_profile(self, data):
        """
        Updates a performance profile.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - ProfilesPerformance or None: Updated performance profile object or None if not found.
        """
        existing_record = self.get_performance_profile_by_symbol(data[0])

        if existing_record:
            existing_record.Name = data[1]
            existing_record.One_Day = data[2]
            existing_record.One_Week = data[3]
            existing_record.One_Month = data[4]
            existing_record.Six_Month = data[5]
            existing_record.Three_Years = data[6]
            existing_record.One_Year = data[7]

            self.session.commit()
            self.logger.info(f"Updated performance profile entry with Symbol: {existing_record.Symbol}")
            return existing_record.Symbol
        else:
            return self.save_performance_profile(data)

    def delete_performance_profile(self, symbol):
        """
        Deletes a performance profile by its Symbol.

        Parameters:
        - symbol (str): Symbol to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        performance_profile = self.session.query(ProfilesPerformance).filter_by(Symbol=symbol).first()
        if performance_profile:
            self.session.delete(performance_profile)
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
        return inspector.has_table(ProfilesPerformance.__tablename__, schema='tgju')

    def create_table(self):
        """
        Create the profiles_performance table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                ProfilesPerformance.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_performance_profile_by_id(self, id):
        """
        Retrieves a performance profile by its id.

        Parameters:
        - symbol (str): Symbol to retrieve.

        Returns:
        - ProfilesPerformance or None: Retrieved performance profile or None if not found.
        """
        return self.session.query(ProfilesPerformance).filter_by(Id=id).first()
