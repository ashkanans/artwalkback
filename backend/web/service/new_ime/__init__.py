from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.ime.main_groups import ImeMainGroups
from backend.web.model.ime.currency import ImeCurrency
from backend.web.model.ime.contract_type import ImeContractType
from backend.web.model.ime.producer_groups import ImeProducerGroups
from backend.web.model.ime.sub_category_grooups import ImeSubCategoryGroups
from backend.web.model.ime.commodity_exchange_amlak import CommodityExchangeAmlak
from backend.web.model.ime.commodity_exchange_arzeh import CommodityExchangeArzeh
from backend.web.model.ime.commodity_exchange_bazare_mali import CommodityExchangeBazareMali
from backend.web.model.ime.commodity_exchange_export import CommodityExchangeExport
from backend.web.model.ime.commodity_exchange_future import CommodityExchangeFuture
from backend.web.model.ime.commodity_exchange_gold import CommodityExchangeGold
from backend.web.model.ime.commodity_exchange_monaghesat import CommodityExchangeMonaghesat
from backend.web.model.ime.commodity_exchange_option import CommodityExchangeOptionBoard
from backend.web.model.ime.commodity_exchange_physical import CommodityExchangePhysical
from backend.web.model.ime.commodity_exchange_premium import CommodityExchangePremium
from backend.web.service.sort_config import SortConfig

engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class NewImeService:
    query_result: list

    def __init__(self):
        self.sortConfig = SortConfig()
        pass

    def get_main_groups(self, sort_by: str, sort_order: str) -> list[ImeMainGroups]:
        config_query = SortConfig().get_config_query(sort_order=sort_order, sort_by=sort_by, model=ImeMainGroups)
        try:
            self.query_result = session.query(ImeMainGroups).from_statement(
                text(f"SELECT * FROM ime.main_groups {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_category_groups(self, sort_by: str, sort_order: str) -> list[ImeMainGroups]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order, model=ImeMainGroups)
        try:
            self.query_result = session.query(ImeMainGroups).from_statement(
                text(f"SELECT * FROM ime.category_groups {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_currency(self, sort_by: str, sort_order: str) -> list[ImeCurrency]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order, model=ImeCurrency)
        try:
            self.query_result = session.query(ImeCurrency).from_statement(
                text(f"SELECT * FROM ime.currency {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_contract_types(self, sort_by: str, sort_order: str) -> list[ImeContractType]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order, model=ImeContractType)
        try:
            self.query_result = session.query(ImeContractType).from_statement(
                text(f"SELECT * FROM ime.contract_type {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_producer_groups(self, sort_by: str, sort_order: str) -> list[ImeProducerGroups]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order, model=ImeProducerGroups)
        try:
            self.query_result = session.query(ImeProducerGroups).from_statement(
                text(f"SELECT * FROM ime.producer_groups {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_sub_category_groups(self, sort_by: str, sort_order: str) -> list[ImeSubCategoryGroups]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order, model=ImeSubCategoryGroups)
        try:
            self.query_result = session.query(ImeSubCategoryGroups).from_statement(
                text(f"SELECT * FROM ime.sub_category_groups {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_amlaks(self, sort_by: str, sort_order: str) -> list[CommodityExchangeAmlak]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order,
                                                     model=CommodityExchangeAmlak)
        try:
            self.query_result = session.query(CommodityExchangeAmlak).from_statement(
                text(f"SELECT * FROM ime.commodity_exchange_amlak {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_arzeh_list(self, sort_by: str, sort_order: str) -> list[CommodityExchangeArzeh]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order,
                                                     model=CommodityExchangeArzeh)
        try:
            self.query_result = session.query(CommodityExchangeArzeh).from_statement(
                text(f"SELECT TOP 1000 * FROM ime.commodity_exchange_arzeh {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_bazare_mali(self, sort_by: str, sort_order: str) -> list[CommodityExchangeBazareMali]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order,
                                                     model=CommodityExchangeBazareMali)
        try:
            self.query_result = session.query(CommodityExchangeBazareMali).from_statement(
                text(f"SELECT * FROM ime.commodity_exchange_bazare_mali {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_exports(self, sort_by: str, sort_order: str) -> list[CommodityExchangeExport]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order,
                                                     model=CommodityExchangeExport)
        try:
            self.query_result = session.query(CommodityExchangeExport).from_statement(
                text(f"SELECT TOP 1000 * FROM ime.commodity_exchange_export {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_future_list(self, sort_by: str, sort_order: str) -> list[CommodityExchangeFuture]:
        config_query = SortConfig().get_config_query(sort_order=sort_order, sort_by=sort_by,
                                                     model=CommodityExchangeFuture)
        try:
            self.query_result = session.query(CommodityExchangeFuture).from_statement(
                text(f"SELECT TOP 100"
                     f" * FROM ime.commodity_exchange_future {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_gold_list(self, sort_by: str, sort_order: str) -> list[CommodityExchangeGold]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order,
                                                     model=CommodityExchangeGold)
        try:
            self.query_result = session.query(CommodityExchangeGold).from_statement(
                text(f"SELECT * FROM ime.commodity_exchange_gold {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_monaghesat_list(self, sort_by: str, sort_order: str) -> list[CommodityExchangeMonaghesat]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order,
                                                     model=CommodityExchangeMonaghesat)
        try:
            self.query_result = session.query(CommodityExchangeMonaghesat).from_statement(
                text(f"SELECT * FROM ime.commodity_exchange_monaghesat {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_option_board_list(self, sort_by: str, sort_order: str) -> list[CommodityExchangeOptionBoard]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order,
                                                     model=CommodityExchangeOptionBoard)
        try:
            self.query_result = session.query(CommodityExchangeOptionBoard).from_statement(
                text(f"SELECT TOP 1000 * FROM ime.commodity_exchange_option_board {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_physical_list(self, sort_by: str, sort_order: str) -> list[CommodityExchangePhysical]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order,
                                                     model=CommodityExchangePhysical)
        try:
            self.query_result = session.query(CommodityExchangePhysical).from_statement(
                text(f"SELECT TOP 10000 * FROM ime.commodity_exchange_physical {config_query}")
            ).all()

        finally:
            session.close()
        return self.query_result

    def get_premium_list(self, sort_by: str, sort_order: str) -> list[CommodityExchangePremium]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order,
                                                     model=CommodityExchangePremium)
        try:
            self.query_result = session.query(CommodityExchangePremium).from_statement(
                text(f"SELECT  * FROM ime.commodity_exchange_premium {config_query}")

            ).all()
        finally:
            session.close()
        return self.query_result
