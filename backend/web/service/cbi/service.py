import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.cbi.yearly_inflation_rate import InflationRate

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class CBIService:
    def __init__(self):
        pass

    def get_combined_dropdown_data(self):
        months = set()
        types = set()
        years = set()

        # Query the table and return the results
        query_result = session.query(InflationRate).from_statement(
            text(
                "SELECT *, [Price index of consumer goods and services] AS price_index FROM estdco.cbi.inflation_rate ORDER BY year DESC;")
        ).all()

        # Extract unique values for each column
        for item in query_result:
            if item.month:
                months.add(item.month)
            if item.type:
                types.add(item.type)
            if item.year:
                years.add(item.year)

        # Convert sets to lists and sort in descending order
        months_sorted = sorted(list(months), reverse=True)
        types_sorted = sorted(list(types), reverse=True)
        years_sorted = sorted(list(years), reverse=True)

        return months_sorted, types_sorted, years_sorted

    def get_relative_data(self, year, month, type):
        start_time = time.time()  # Record the start time

        query_data = session.query(InflationRate).from_statement(
            text(
                f"SELECT * FROM cbi.filtered_inflation_rate(:year, :month, :type) ")
        ).params(year=year, month=month, type=type).all()

        end_time = time.time()  # Record the end time
        elapsed_time = end_time - start_time  # Calculate the elapsed time
        print(f"{len(query_data)} of rows found")
        print(f"Query execution time: {elapsed_time} seconds")

        return query_data
