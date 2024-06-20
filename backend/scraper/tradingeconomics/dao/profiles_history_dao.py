from datetime import datetime

from sqlalchemy import inspect, and_, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.tradingeconomics.model.profiles_history import ProfilesHistory

Base = declarative_base()


class ProfilesHistoryDao:
    def __init__(self, session: Session):
        """
        Initializes the ProfilesHistoryDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_profiles_history(self, data):
        """
        Saves a new ProfilesHistory entry.

        Parameters:
        - data (dict): Dictionary containing ProfilesHistory data.

        Returns:
        - ProfilesHistory: Saved ProfilesHistory object.
        """
        profiles_history = ProfilesHistory(**data)
        self.session.add(profiles_history)
        self.session.commit()
        return profiles_history

    def get_all_profiles_histories(self):
        """
        Retrieves all ProfilesHistory entries.

        Returns:
        - list: List of all ProfilesHistory entries.
        """
        return self.session.query(ProfilesHistory).all()

    def get_profiles_history_by_ann_id(self, ann_id):
        """
        Retrieves a ProfilesHistory entry by its AnnID.

        Parameters:
        - ann_id (str): AnnID to retrieve.

        Returns:
        - ProfilesHistory or None: Retrieved ProfilesHistory or None if not found.
        """
        return self.session.query(ProfilesHistory).filter_by(AnnID=ann_id).first()

    def get_profiles_history_by_one_month_period_until(self, one_month_period_until):
        """
        Retrieves a ProfilesHistory entry by its One_Month_Period_Until.

        Parameters:
        - one_month_period_until (str): One_Month_Period_Until to retrieve.

        Returns:
        - ProfilesHistory or None: Retrieved ProfilesHistory or None if not found.
        """
        return self.session.query(ProfilesHistory).filter_by(One_Month_Period_Until=one_month_period_until).first()

    def update_profiles_history(self, data):
        """
        Updates a ProfilesHistory entry.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - ProfilesHistory or None: Updated ProfilesHistory object or None if not found.
        """
        existing_record = self.session.query(ProfilesHistory).filter_by(AnnID=data.get("AnnID"),
                                                                        date=data.get("date")).first()
        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)
            self.session.commit()
            return existing_record.AnnID
        else:
            return self.save_profiles_history(data)

    def delete_profiles_history(self, ann_id):
        """
        Deletes a ProfilesHistory entry by its AnnID.

        Parameters:
        - ann_id (str): AnnID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        profiles_history = self.session.query(ProfilesHistory).filter_by(AnnID=ann_id).first()
        if profiles_history:
            self.session.delete(profiles_history)
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
        return inspector.has_table(ProfilesHistory.__tablename__)

    def create_table(self):
        """
        Create the profiles_history table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                print("Creating table...")
                ProfilesHistory.__table__.create(self.session.bind)
                self.session.commit()
                print("Table created.")
                return True
            except Exception as e:
                print(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        print("Table already exists.")
        return False

    def get_first_price_by_AnnId_and_year(self, annId, year):
        year_start = datetime(int(year), 1, 1)
        year_end = datetime(int(year), 12, 20)

        # Query the database to get the first price for the given AnnId and year
        result = (
            self.session.query(ProfilesHistory)
            .filter(and_(ProfilesHistory.AnnID == annId,
                         ProfilesHistory.date >= year_start,
                         ProfilesHistory.date <= year_end))
            .order_by(ProfilesHistory.date)
            .first()
        )

        # Return the price if any result is found
        return result.price if result else None

    def get_last_price_by_AnnId(self, annId):
        result = (
            self.session.query(ProfilesHistory)
            .filter(ProfilesHistory.AnnID == annId)
            .order_by(desc(ProfilesHistory.date))
            .first()
        )

        # Return the price if any result is found
        return result.price if result else None
