from sqlalchemy import inspect
from sqlalchemy.orm import declarative_base

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tgju.model.profiles_at_a_glance import ProfilesAtAGlance

Base = declarative_base()


class ProfilesAtAGlanceDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        """
        Initializes the ProfilesAtAGlanceDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_profile_at_a_glance(self, data):
        """
        Saves a new profile at a glance.

        Parameters:
        - data (dict): Dictionary containing profile at a glance data.

        Returns:
        - ProfilesAtAGlance: Saved profile at a glance object.
        """
        profile_at_a_glance = ProfilesAtAGlance(data)
        self.session.add(profile_at_a_glance)
        self.session.commit()
        self.logger.info(f"Saved profile at a glance entry with symbol: {profile_at_a_glance.Symbol}")
        return profile_at_a_glance

    def get_all_profiles_at_a_glance(self):
        """
        Retrieves all profiles at a glance.

        Returns:
        - list: List of all profiles at a glance.
        """
        return self.session.query(ProfilesAtAGlance).all()

    def get_profile_at_a_glance_by_symbol(self, symbol):
        """
        Retrieves a profile at a glance by its symbol.

        Parameters:
        - symbol (str): Profile at a glance symbol to retrieve.

        Returns:
        - ProfilesAtAGlance or None: Retrieved profile at a glance or None if not found.
        """
        return self.session.query(ProfilesAtAGlance).filter_by(Symbol=symbol).first()

    def update_profile_at_a_glance(self, data):
        """
        Updates a profile at a glance.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - ProfilesAtAGlance or None: Updated profile at a glance object or None if not found.
        """
        existing_record = self.get_profile_at_a_glance_by_symbol(data[0])

        if existing_record:

            existing_record.CurrentRate = data[1]
            existing_record.HighestDailyPrice = data[2]
            existing_record.LowestDailyPrice = data[3]
            existing_record.MaxDailyFluctuation = data[4]
            existing_record.MaxFluctuationPercentage = data[5]
            existing_record.MarketOpeningRate = data[6]
            existing_record.LastRateRegistrationTime = data[7]
            existing_record.PreviousDayRate = data[8]
            existing_record.ChangePercentage = data[9]
            existing_record.ChangeAmount = data[10]

            self.session.commit()
            self.logger.info(f"Updated profile at a glance entry with symbol: {existing_record.Symbol}")
            return existing_record.Symbol
        else:
            return self.save_profile_at_a_glance(data)

    def delete_profile_at_a_glance(self, symbol):
        """
        Deletes a profile at a glance by its symbol.

        Parameters:
        - symbol (str): Profile at a glance symbol to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        profile_at_a_glance = self.session.query(ProfilesAtAGlance).filter_by(Symbol=symbol).first()
        if profile_at_a_glance:
            self.session.delete(profile_at_a_glance)
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
        return inspector.has_table(ProfilesAtAGlance.__tablename__, schema='tgju')

    def create_table(self):
        """
        Create the profiles_at_a_glance table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                ProfilesAtAGlance.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        return False
