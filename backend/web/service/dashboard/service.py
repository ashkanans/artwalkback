import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.dashboard.card_data import CardData
from backend.web.model.dashboard.export_barchart import ExportBarchart
from backend.web.model.dashboard.first_page_tables_rows import FirstPageTablesRows


class DashboardService:
    def __init__(self):
        # Creating the SQLAlchemy engine
        engine = create_engine(SQL_SERVER_URL)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_physical_card_data_by_date(self, date, period):
        start_time = time.time()  # Record the start time

        query_data = self.session.query(CardData).from_statement(
            text(
                f"SELECT * FROM ime.GetPhysicalSummaryData(:InputDate, :datePeriod)")
        ).params(InputDate=date, datePeriod=period).all()

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"{len(query_data)} of rows found")
        print(f"Query execution time: {elapsed_time} seconds")

        return query_data

    def get_export_card_data_by_date(self, date, period):
        start_time = time.time()  # Record the start time

        query_data = self.session.query(CardData).from_statement(
            text(
                f"SELECT * FROM ime.GetExportSummaryData(:InputDate, :datePeriod)")
        ).params(InputDate=date, datePeriod=period).all()

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"{len(query_data)} of rows found")
        print(f"Query execution time: {elapsed_time} seconds")

        return query_data

    def get_offer_card_data_by_date(self, date, period):
        start_time = time.time()  # Record the start time

        query_data = self.session.query(CardData).from_statement(
            text(
                f"SELECT * FROM ime.GetOfferSummaryData(:InputDate, :datePeriod)")
        ).params(InputDate=date, datePeriod=period).all()

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"{len(query_data)} of rows found")
        print(f"Query execution time: {elapsed_time} seconds")

        return query_data

    def get_premium_card_data_by_date(self, date, period):
        start_time = time.time()  # Record the start time

        query_data = self.session.query(CardData).from_statement(
            text(
                f"SELECT * FROM ime.GetPremiumSummaryData(:InputDate, :datePeriod)")
        ).params(InputDate=date, datePeriod=period).all()

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"{len(query_data)} of rows found")
        print(f"Query execution time: {elapsed_time} seconds")

        return query_data

    def get_dashboard_ime_physical_barChart_data(self, date, period):
        start_time = time.time()  # Record the start time

        query_data = self.session.query(CardData).from_statement(
            text(
                f"SELECT * FROM ime.GetDailyPhysicalSummaryData(:InputDate, :datePeriod) OPTION (MAXRECURSION 0);")
        ).params(InputDate=date, datePeriod=period).all()

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"{len(query_data)} of rows found")
        print(f"Query execution time: {elapsed_time} seconds")

        return query_data

    def get_dashboard_ime_export_barChart_data(self, date, period):
        start_time = time.time()  # Record the start time

        query_data = self.session.query(ExportBarchart).from_statement(
            text(
                f"SELECT * FROM ime.GetDailyExportSummaryData(:InputDate, :datePeriod) OPTION (MAXRECURSION 0);")
        ).params(InputDate=date, datePeriod=period).all()

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"{len(query_data)} of rows found")
        print(f"Query execution time: {elapsed_time} seconds")

        return query_data

    def get_first_page_tables_rows(self):
        query_result_tgju = self.session.query(FirstPageTablesRows).from_statement(
            text("SELECT * FROM web.first_page_tables_rows_tgju")
        ).all()

        query_result_tsetmc = self.session.query(FirstPageTablesRows).from_statement(
            text("SELECT * FROM web.first_page_tables_rows_tsetmc")
        ).all()

        return query_result_tgju, query_result_tsetmc
