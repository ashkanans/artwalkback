from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.business_insider.id import BusinessInsiderID
from backend.web.model.business_insider.price_history import PriceHistory

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class BIService:
    def __init__(self):
        pass

    def get_bi_ids(self):
        # Query the view and return the results
        query_result = session.query(BusinessInsiderID).from_statement(
            text("SELECT [category_id],[category_fa], [ID], [Name_fa], [type] FROM [estdco].[app].[chart_IDs]")
        ).all()

        return query_result

    def get_relative_data(self, id=None, from_date=None, to_date=None, date_type=None):
        date_type = "" if date_type is None else date_type
        sql_query = text(
            f"SELECT * FROM (SELECT *, TRY_CONVERT(DATE, REPLACE(Date, '/', '-'), 111) AS ConvertedDate "
            f"FROM businessinsider.filtered_price_histories(:from_date, :to_date, :id, :date_type)) AS Subquery "
            "ORDER BY ConvertedDate ASC"
        )

        query_data = session.query(PriceHistory).from_statement(
            sql_query
        ).params(from_date=from_date, to_date=to_date, id=id, date_type=date_type).all()
        return query_data

    def get_bi_ids_by_id(self, id):
        query_result = session.query(BusinessInsiderID).from_statement(
            text("SELECT [category_id],[category_fa], [ID], [Name_fa], [type] FROM [estdco].[app].[chart_IDs]"
                 f"WHERE [ID] = {id}")
        ).one()

        return query_result
