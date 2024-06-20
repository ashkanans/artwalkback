from sqlalchemy import inspect, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from backend.scraper.logger.base_logger import BaseLogger
from backend.scraper.tsetmc.model.top_trade_most_visited import TradeTopMostVisited

Base = declarative_base()


class TradeTopMostVisitedDao(BaseLogger):
    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the TradeTopMostVisitedDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_trade_top_most_visited(self, data):
        """
        Saves a new trade top most visited entry.

        Parameters:
        - data (dict): Dictionary containing trade top most visited data.

        Returns:
        - int: Saved trade top most visited entry's insCode
        """
        trade_top_most_visited = TradeTopMostVisited(**data)
        self.session.add(trade_top_most_visited)
        self.session.commit()
        self.logger.info(f"Saved trade top most visited entry. insCode: {trade_top_most_visited.insCode}")
        return trade_top_most_visited.insCode

    def get_all_trade_top_most_visited_entries(self):
        """
        Retrieves all trade top most visited entries.

        Returns:
        - list: List of all trade top most visited entries.
        """
        return self.session.query(TradeTopMostVisited).all()

    def get_trade_top_most_visited_by_insCode(self, entry_id):
        """
        Retrieves a trade top most visited entry by its ID.

        Parameters:
        - entry_id (int): Trade top most visited entry ID to retrieve.

        Returns:
        - TradeTopMostVisited or None: Retrieved trade top most visited entry or None if not found.
        """
        return self.session.query(TradeTopMostVisited).filter_by(insCode=entry_id).first()

    def get_trade_top_most_visited_by_marketName(self, marketName):
        """
        Retrieves a trade top most visited entry by its ID.

        Parameters:
        - entry_id (int): Trade top most visited entry ID to retrieve.

        Returns:
        - TradeTopMostVisited or None: Retrieved trade top most visited entry or None if not found.
        """
        return self.session.query(TradeTopMostVisited).filter_by(marketName=marketName).first()

    def update_trade_top_most_visited(self, data):
        """
        Updates a trade top most visited entry.

        Parameters:
        - entry_id (int): Trade top most visited entry ID to update.
        - data (dict): Dictionary containing updated data.

        Returns:
        - int: Updated trade top most visited entry's ID
        """

        existing_record = self.get_trade_top_most_visited_by_insCode(data.get("insCode"))
        if existing_record:
            for key, value in data.items():
                setattr(existing_record, key, value)

            self.session.commit()
            self.logger.info(f"Updated trade top most visited entry. insCode: {existing_record.insCode}")
            return existing_record.id

        else:
            return self.save_trade_top_most_visited(data)

    def delete_trade_top_most_visited_by_insCode(self, entry_id):
        """
        Deletes a trade top most visited entry by its ID.

        Parameters:
        - entry_id (int): Trade top most visited entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        trade_top_most_visited = self.session.query(TradeTopMostVisited).filter_by(insCode=entry_id).first()
        if trade_top_most_visited:
            self.session.delete(trade_top_most_visited)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the trade_top_most_visited table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(TradeTopMostVisited.__tablename__)

    def create_table(self):
        """
        Create the tse_trade_top_most_visited table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                TradeTopMostVisited.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_insCodes_by_marketName(self, marketName):
        """
        Retrieves insCode values for a given marketName using the stored procedure.

        Parameters:
        - marketName (str): The marketName to query.

        Returns:
        - list: List of insCode values.
        """
        # Define the stored procedure call
        sp_call = text("EXEC GetInsCodesByMarketName @InputMarketName = :market_name")

        # Execute the stored procedure and fetch the result
        result = self.session.execute(sp_call, {"market_name": marketName})

        # Extract insCode values from the result
        insCodes = [row[0] for row in result]

        return insCodes
