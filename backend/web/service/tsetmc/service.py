from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.oilprice.id import OilPriceID
from backend.web.model.tsetmc.entered_money_model import EnteredMoneyRank
from backend.web.model.tsetmc.option import Option
from backend.web.model.tsetmc.return_info import ReturnInfo
from backend.web.model.tsetmc.stocks_info import StockInfo
from backend.web.model.tsetmc.Important_filters import ImportantFilters
from backend.web.service.sort_config import SortConfig

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class TsetmcService:
    query_result: list

    def __init__(self):
        self.sortConfig = SortConfig()
        pass

    def get_combined_dropdown_data(self, sort_by: str, sort_order: str) -> list[OilPriceID]:
        config_query = SortConfig().get_config_query(sort_order=sort_order, sort_by=sort_by, model=OilPriceID)
        try:
            self.query_result = session.query(OilPriceID).from_statement(
                text(f"SELECT * FROM oilprice.ID WHERE blend_name IS NOT NULL {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_return_info(self, sort_by: str, sort_order: str) -> list[ReturnInfo]:
        config_query = SortConfig().get_config_query(sort_order=sort_order, sort_by=sort_by, model=ReturnInfo)
        try:
            self.query_result = session.query(ReturnInfo).from_statement(
                text(
                    f"SELECT [tse_id] ,[return] AS [return_value] ,[symbol] ,[type] ,[index_type] ,[rank] FROM [estdco].[app].[return_info] {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_entered_money(self, sort_by: str, sort_order: str) -> list[EnteredMoneyRank]:
        config_query = SortConfig().get_config_query(sort_order=sort_order, sort_by=sort_by, model=EnteredMoneyRank)
        try:
            self.query_result = session.query(EnteredMoneyRank).from_statement(
                text(
                    f"SELECT [tse_id] ,[type],[entered_money],[rank],[type_rank],[Persian symbol] AS [Persian_symbol],[type_report] FROM [estdco].[app].[entered_money_rank] {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_stocks_info(self, sort_by: str, sort_order: str):
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order, model=StockInfo)
        try:
            self.query_result = session.query(StockInfo).from_statement(
                text(f"SELECT [Company Name] As [Company_Name], [Persian symbol] As [Persian_Symbol], [Industry Group] As [Industry_Group], [queue value] As [queue_value] , * FROM [app].[stocks_info] {config_query}")).all()
        finally:
            session.close()

        return self.query_result

    def get_important_filters(self, sort_by: str, sort_order: str) -> list[ImportantFilters]:
        config_query = SortConfig().get_config_query(sort_by=sort_by, sort_order=sort_order, model=ImportantFilters)
        try:
            self.query_result = session.query(ImportantFilters).from_statement(
                text(f"SELECT *, [queue value] AS [queue_value] FROM [estdco].[app].[Important_filters] {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_options(self, sort_by=None):
        results = {}
        ids = self.get_unique_ids()
        for id in ids:
            sql_query = text(f"""
                SELECT 
                    *, 
                    [break even] as [break_even], 
                    [Black-Scholes] as [Black_Scholes],
                    [Expected return on stocks] as [Expected_return_on_stocks],
                    [diff_Black–Scholes] as [diff_Black_Scholes]
                FROM [estdco].[app].[option]
                WHERE id = {id}
            """)

            query_result = session.query(Option).from_statement(
                sql_query
            ).all()

            results[id] = query_result
        return results

    def get_unique_ids(self):
        sql_query = text("""
            SELECT DISTINCT id
            FROM [estdco].[app].[option]
        """)

        query_result = session.execute(sql_query)
        unique_ids = [int(row[0]) for row in query_result]

        unique_ids.sort()
        return unique_ids

# service = TsetmcService().get_stocks_info()
