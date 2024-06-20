from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.scraper.ime.dao.physical_transaction_dao import PhysicalTransactionDao
from backend.scraper.logger.base_logger import BaseLogger

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class PhysicalTransactionService(BaseLogger):
    def __init__(self):
        """
        Initializes the PhysicalTransactionService.

        Parameters:
        - session: SQLAlchemy session object
        """
        self.physical_transaction_info_dao = PhysicalTransactionDao(session)

    def save_physical_transaction_info(self, data):
        """
        Saves a new physical transaction info entry.

        Parameters:
        - data (list of dict): List of Dictionary containing updated data.

        Returns:
        - int: Saved physical transaction info entry's ID
        """
        return self.physical_transaction_info_dao.save_physical_transaction_info(data)

    def get_all_physical_transaction_info_entries(self):
        """
        Retrieves all physical transaction info entries.

        Returns:
        - list: List of all physical transaction info entries.
        """
        return self.physical_transaction_info_dao.get_all_physical_transaction_info_entries()

    def get_physical_transaction_info_by_id(self, Symbol, ContractType, datetaghaza, ArzeBasePrice, cBrokerSpcName,
                                            ArzehKonandeh, Arze, Tasvieh):
        """
        Retrieves a physical transaction info entry by its ID.

        Parameters:
        - name (str): physical transaction info entry ID to retrieve.

        Returns:
        - PhysicalTransaction or None: Retrieved physical transaction info entry or None if not found.
        """
        return self.physical_transaction_info_dao.get_physical_transaction_info_by_id_dao(Symbol, ContractType,
                                                                                          datetaghaza, ArzeBasePrice,
                                                                                          cBrokerSpcName, ArzehKonandeh,
                                                                                          Arze, Tasvieh)

    def update_physical_transaction_info(self, data):
        """
        Updates a physical transaction info entry.

        Parameters:
        - name (str): physical transaction info entry ID to update.
        - data (list of dict): List of Dictionary containing updated data.

        Returns:
        - str: Updated physical transaction info entry's ID
        """

        return self.physical_transaction_info_dao.update_physical_transaction_info(data)

    def delete_physical_transaction_info_by_id(self, id):
        """
        Deletes a physical transaction info entry by its ID.

        Parameters:
        - name (str): physical transaction info entry ID to delete.

        Returns:
        - bool: True if deletion successful, False otherwise.
        """
        return self.physical_transaction_info_dao.delete_physical_transaction_info_by_id(id)

    def create_table(self):
        """
        Create the physical transaction table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.physical_transaction_info_dao.create_table()

    def get_all_ins_ids(self):
        """
        Retrieves all persian symbols.

        Returns:
        - list: List of all persian symbols.
        """
        return self.physical_transaction_info_dao.get_all_ins_ids()

    def table_exists(self):
        """
        Create the physical transaction info table in the database.

        Returns:
        - bool: True if the table is created successfully, False otherwise.
        """
        return self.physical_transaction_info_dao.table_exists()

    def get_first_transaction_by_GoodsName_and_year(self, goodsName, year):
        return self.physical_transaction_info_dao.get_first_transaction_by_GoodsName_and_year(goodsName, year)

    def get_last_transaction_by_GoodsName_and_year(self, goodsName):
        return self.physical_transaction_info_dao.get_last_transaction_by_GoodsName_and_year(goodsName)

    def calc_weighted_average_GoodsName_by_year(self, goodsName, year):
        return self.physical_transaction_info_dao.calc_weighted_average_GoodsName_by_year(goodsName, year)
