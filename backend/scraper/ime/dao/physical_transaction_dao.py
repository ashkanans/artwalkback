from datetime import datetime

from khayyam import JalaliDate
from sqlalchemy import inspect, and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

from backend.scraper.ime.model.physical_transaction import PhysicalTransaction
from backend.scraper.logger.base_logger import BaseLogger

Base = declarative_base()


class PhysicalTransactionDao(BaseLogger):
    def __init__(self, session: Session):
        super().__init__()
        """
        Initializes the PhysicalTransactionDao.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.session = session

    def save_physical_transaction_info(self, data):
        """
        Saves a new physical transaction info entry.

        Parameters:
        - data (List of dict): list of Dictionary containing updated data.

        Returns:
        - int: Saved physical transaction info entry's ID
        """
        physical_transaction_info = PhysicalTransaction(**data)
        self.session.add(physical_transaction_info)
        self.session.commit()
        self.logger.info(f"Saved physical transaction info entry with ID: {physical_transaction_info.GoodsName}")
        return physical_transaction_info.id

    def get_all_physical_transaction_info_entries(self):
        """
        Retrieves all physical transaction info entries.

        Returns:
        - list: List of all physical transaction info entries.
        """
        return self.session.query(PhysicalTransaction).all()

    def get_physical_transaction_info_by_id_dao(self, Symbol, contractType, Date, taghaza, azrzeBasePrice,
                                                CBrokerSpcName, arzehKonandeh, Arze, tasvieh):
        """
        Retrieves a physical transaction info entry by its ID.

        Parameters:
        - id (str): physical transaction info entry ID to retrieve.

        Returns:
        - physical transaction or None: Retrieved physical transaction info entry or None if not found.
        """
        return self.session.query(PhysicalTransaction).filter_by(Symbol=Symbol).filter_by(
            ContractType=contractType).filter_by(date=Date).filter_by(ArzeBasePrice=azrzeBasePrice).filter_by(
            taghaza=taghaza).filter_by(cBrokerSpcName=CBrokerSpcName).filter_by(ArzehKonandeh=arzehKonandeh).filter_by(
            arze=Arze).filter_by(Tasvieh=tasvieh).first()

    def update_physical_transaction_info(self, data):
        """
        Updates a physical transaction info entry.

        Parameters:
        - data (List of dict): list of Dictionary containing updated data.

        Returns:
        - str: Updated physical transaction info entry's ID
        """
        updated_ids = []
        for item in data:
            try:
                existing_record = self.get_physical_transaction_info_by_id_dao(item.get("Symbol"),
                                                                               item.get("ContractType"),
                                                                               item.get("date"), item.get("taghaza"),
                                                                               item.get("ArzeBasePrice"),
                                                                               item.get("cBrokerSpcName"),
                                                                               item.get("ArzehKonandeh"),
                                                                               item.get("arze"), item.get("Tasvieh"))
                if existing_record:
                    for key, value in item.items():
                        setattr(existing_record, key, value)

                    self.session.commit()
                    self.logger.info(f"Updated physical transaction info entry with ID: {existing_record.GoodsName}")
                    updated_ids.append(existing_record.id)
                else:
                    self.save_physical_transaction_info(item)

            except NoResultFound:
                updated_ids.append(self.save_physical_transaction_info(item))

        return updated_ids

    def delete_physical_transaction_info_by_id(self, id):
        """
        Deletes a physical transaction info entry by its ID.

        Parameters:
        - id (str): physical transaction info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        physical_transaction = self.session.query(PhysicalTransaction).filter_by(id=id).first()
        if physical_transaction:
            self.session.delete(physical_transaction)
            self.session.commit()
            return True
        return False

    def table_exists(self):
        """
        Check if the physical transaction table exists in the database.

        Returns:
        - bool: True if the table exists, False otherwise.
        """
        inspector = inspect(self.session.bind)
        return inspector.has_table(PhysicalTransaction.__tablename__)

    def create_table(self):
        """
        Create the ime_physical_transaction table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        if not self.table_exists():
            try:
                self.logger.info("Creating table...")
                PhysicalTransaction.__table__.create(self.session.bind)
                self.session.commit()
                self.logger.info("Table created.")
                return True
            except Exception as e:
                self.logger.exception(f"Error creating table: {e}")
                self.session.rollback()  # Rollback in case of an error
                return False
        self.logger.info("Table already exists.")
        return False

    def get_all_ins_ids(self):
        """
        Retrieves all values in the id column.

        Parameters:
        - session: SQLAlchemy session object

        Returns:
        - list: List of all values in the id column.
        """
        id_values = self.session.query(PhysicalTransaction.id).all()
        return [value[0] for value in id_values]

    def get_first_transaction_by_GoodsName_and_year(self, goodsName, year):
        year_start = datetime(int(year), 1, 1)
        year_end = datetime(int(year), 12, 31)

        # Query the database to get the earliest transaction for the given goodsName and year
        result = (
            self.session.query(PhysicalTransaction)
            .filter(and_(PhysicalTransaction.GoodsName == goodsName,
                         PhysicalTransaction.date >= year_start,
                         PhysicalTransaction.date <= year_end))
            .order_by(PhysicalTransaction.date)
            .first()
        )

        return result

    def get_first_transaction_by_GoodsName_and_year(self, goodsName, year):
        year_start = datetime(int(year), 1, 1)
        year_end = datetime(int(year), 12, 31)

        # Query the database to get the earliest transaction for the given goodsName and year
        result = (
            self.session.query(PhysicalTransaction)
            .filter(and_(PhysicalTransaction.GoodsName == goodsName,
                         PhysicalTransaction.date >= year_start,
                         PhysicalTransaction.date <= year_end))
            .order_by(PhysicalTransaction.date)
            .first()
        )

        return result

    def calc_weighted_average_GoodsName_by_year(self, goodsName, year):
        year_start_jalali = JalaliDate(int(year), 1, 1)
        year_end_jalali = JalaliDate(int(year), 12, 29)
        year_start = year_start_jalali.strftime("%Y/%m/%d")
        year_end = year_end_jalali.strftime("%Y/%m/%d")
        result = (self.session.query(PhysicalTransaction).filter(and_(PhysicalTransaction.GoodsName == goodsName,
                                                                      PhysicalTransaction.date >= year_start,
                                                                      PhysicalTransaction.date <= year_end))
                  .order_by(PhysicalTransaction.date).all())

        # Convert strings to floats, skip where 'MinPrice' or 'Quantity' is null or empty
        # numerator
        sigma_price_vol = sum(float(res.Quantity) * float(res.MinPrice)
                              for res in result
                              if res.Quantity and res.Quantity.strip()
                              and res.MinPrice and res.MinPrice.strip())

        # denominator
        sigma_vol = sum(float(res.Quantity)
                        for res in result
                        if res.Quantity and res.Quantity.strip())

        if sigma_price_vol > 0 and sigma_vol > 0:
            return sigma_price_vol / sigma_vol
        else:
            return 0
