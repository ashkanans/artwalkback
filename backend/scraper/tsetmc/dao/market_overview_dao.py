from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.market_overview import MarketOverview

Base = declarative_base()


class MarketOverviewDao(BaseLogger):
    def __init__(self, session):
        super().__init__()
        """
        Initializes the MarketOverviewDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_market_overview(self, data, id):
        """
        Saves a new market overview.

        Parameters:
        - data (dict): Dictionary containing market overview data.

        Returns:
        - MarketOverview: Saved market overview object.
        """
        market_overview = MarketOverview(**data)
        self.session.add(market_overview)
        self.session.commit()
        self.logger.info(f"Saved market overview entry with ID: {id}")
        return market_overview

    def get_all_market_overviews(self):
        """
        Retrieves all market overviews.

        Returns:
        - list: List of all market overviews.
        """
        return self.session.query(MarketOverview).all()

    def get_market_overview_by_name(self, market_overview_name):
        """
        Retrieves a market overview by its name.

        Parameters:
        - market_overview_name (int): Market overview name to retrieve.

        Returns:
        - MarketOverview or None: Retrieved market overview or None if not found.
        """
        return self.session.query(MarketOverview).filter_by(name=market_overview_name).first()

    def update_market_overview(self, data, id):
        """
        Updates a market overview.

        Parameters:
        - data (dict): Dictionary containing updated data.

        Returns:
        - MarketOverview or None: Updated market overview object or None if not found.
        """
        existing_record = self.get_market_overview_by_name(data.get("name"))

        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)
            self.session.commit()
            self.logger.info(f"Updated market overview entry with ID: {id}")
            return existing_record.name
        else:
            return self.save_market_overview(data, id)

    def delete_market_overview(self, market_overview_name):
        """
        Deletes a market overview by its name.

        Parameters:
        - market_overview_name (int): Market overview name to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        market_overview = self.session.query(MarketOverview).filter_by(name=market_overview_name).first()
        if market_overview:
            self.session.delete(market_overview)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the specified table exists in the database.

        Parameters:
        - table_name (str): The name of the table to check.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(MarketOverview.__tablename__)

    def create_table(self):
        """
        Create the tse_market_overview table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                MarketOverview.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.info(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False
