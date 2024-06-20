import time
from collections import defaultdict

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.ime.combined_dropdown_data import CombinedDropdownData
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
from backend.web.model.ime.sources import Sources

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class ImeService:
    def __init__(self):
        pass

    def get_combined_dropdown_data(self):
        # Query the view and return the results
        query_result = session.query(CombinedDropdownData).from_statement(
            text("SELECT * FROM ime.combined_dropdown_data ORDER BY CAST([code] AS INT) ASC;")
        ).all()

        # Initialize a defaultdict to store data
        data_dict = defaultdict(list)

        # Organize the data into a dictionary of lists
        for row in query_result:
            data_dict[row.TableName].append({"code": row.code, "Name": row.Name, "TableNameMap": row.Name})

        return data_dict

    def get_relative_data(self, source_type=None, from_date=None, to_date=None, main_group=None, category_group=None,
                          sub_category_group=None,
                          producer_group=None):

        print(f"source value: {source_type}")
        print(f"type: {type(source_type)}")
        print(f"main_group value: {main_group}")
        print(f"producer_group: {producer_group}")

        source_type = str(source_type)
        main_group = None
        category_group = None
        sub_category_group = None
        producer_group = None

        from_date = from_date
        to_date = to_date

        query_type = session.query(Sources).from_statement(
            text("SELECT * FROM ime.sources WHERE code = :code")
        ).params(code=source_type).first()

        table_name = query_type.TableNameMap
        query_data = None
        start_time = time.time()

        if source_type == "1":

            query_data = session.query(CommodityExchangeArzeh).from_statement(
                text(
                    f"SELECT * FROM ime.filtered_commodity_exchange_arzeh(:from_date, :to_date, :producerId, :mainGroupId, :categoryGroup, :subCategoryGroup)")
            ).params(from_date=from_date, to_date=to_date, producerId=producer_group, mainGroupId=main_group,
                     categoryGroup=category_group, subCategoryGroup=sub_category_group).all()

        elif source_type == "2":

            category = None

            if main_group:

                category = str(main_group)

                if category_group:

                    category += "-" + str(category_group)

                    if sub_category_group:
                        category += "-" + str(sub_category_group)

            query_data = session.query(CommodityExchangePhysical).from_statement(

                text(

                    f"SELECT * FROM ime.filtered_commodity_exchange_physical(:from_date, :to_date, :producerId, :category)")

            ).params(from_date=from_date, to_date=to_date, producerId=producer_group, category=category).all()

        elif source_type == "3":

            query_data = session.query(CommodityExchangeExport).from_statement(
                text(
                    f"SELECT * FROM ime.filtered_commodity_exchange_export(:from_date, :to_date, :producerId, :mainGroupId, :categoryGroup, :subCategoryGroup)")
            ).params(from_date=from_date, to_date=to_date, producerId=producer_group, mainGroupId=main_group,
                     categoryGroup=category_group, subCategoryGroup=sub_category_group).all()

        elif source_type == "4":

            query_data = session.query(CommodityExchangePremium).from_statement(
                text(
                    f"SELECT * FROM ime.filtered_commodity_exchange_premium(:from_date, :to_date)")
            ).params(from_date=from_date, to_date=to_date).all()

        elif source_type == "5":

            query_data = session.query(CommodityExchangeAmlak).from_statement(
                text(
                    f"SELECT * FROM ime.filtered_commodity_exchange_amlak(:from_date, :to_date)")
            ).params(from_date=from_date, to_date=to_date).all()

        elif source_type == "6":

            query_data = session.query(CommodityExchangeMonaghesat).from_statement(
                text(
                    f"SELECT * FROM ime.filtered_commodity_exchange_monaghesat(:from_date, :to_date)")
            ).params(from_date=from_date, to_date=to_date).all()

        elif source_type == "7":

            query_data = session.query(CommodityExchangeFuture).from_statement(
                text(
                    f"SELECT * FROM ime.filtered_commodity_exchange_future(:from_date, :to_date)")
            ).params(from_date=from_date, to_date=to_date).all()

        elif source_type == "8":

            query_data = session.query(CommodityExchangeOptionBoard).from_statement(
                text(
                    f"SELECT * FROM ime.filtered_commodity_exchange_option(:from_date, :to_date)")
            ).params(from_date=from_date, to_date=to_date).all()

        elif source_type == "9":

            query_data = session.query(CommodityExchangeBazareMali).from_statement(
                text(
                    f"SELECT * FROM ime.filtered_commodity_exchange_financail_market(:from_date, :to_date)")
            ).params(from_date=from_date, to_date=to_date).all()

        elif source_type == "10":

            query_data = session.query(CommodityExchangeGold).from_statement(
                text(
                    f"SELECT * FROM ime.filtered_commodity_exchange_gold(:from_date, :to_date)")
            ).params(from_date=from_date, to_date=to_date).all()

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"{len(query_data)} of rows found")
        print(f"Query execution time: {elapsed_time} seconds")
        print(f"type: {type(query_data)}")
        return query_data, table_name

    def summary_info(self, source_type=None, from_date=None, to_date=None, main_group=None, category_group=None,
                     sub_category_group=None,
                     producer_group=None):

        input_date = '2024/03/26'
        query_data = session.query(CommodityExchangeExport).from_statement(
            text(
                f"EXEC @return_value = [ime].[GetPhysicalSummaryData] @InputDate = N'{input_date}'")
        ).all()

        return query_data
