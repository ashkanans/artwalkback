import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.oilprice.id import OilPriceID
from backend.web.model.oilprice.price_archive import PriceArchive

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class OilPriceService:
    def __init__(self):
        pass

    def get_combined_dropdown_data(self):
        # Query the view and return the results
        query_result = session.query(OilPriceID).from_statement(
            text("SELECT * FROM oilprice.ID WHERE blend_name IS NOT NULL")
        ).all()

        return query_result

    def get_relative_data(self, chosen_id, to_date, from_date):
        start_time = time.time()
        query_data = session.query(PriceArchive).from_statement(
            text(
                f"SELECT * FROM oilprice.filtered_price_archives(:from_date, :to_date, :id) ORDER BY time DESC")
        ).params(from_date=from_date, to_date=to_date, id=chosen_id).all()

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Number of rows found: {len(query_data)}")
        print(f"Query execution time: {elapsed_time} seconds")

        return query_data
