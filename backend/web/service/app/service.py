from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.app.chart_data import ChartData
from backend.web.model.app.chart_id import ChartIDs

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()

from backend.web.service.sort_config import SortConfig


class AppService:
    def __init__(self):
        self.sortConfig = SortConfig()
        self.query_result: list = []
        pass

    def get_chart_ids(self, sort_by: str, sort_order: str) -> list[ChartIDs]:
        config_query = SortConfig().get_config_query(sort_order=sort_order, sort_by=sort_by, model=ChartIDs)
        try:
            self.query_result = session.query(ChartIDs).from_statement(
                text(f"SELECT * FROM [estdco].[app].[chart_IDs] {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result

    def get_chart_data(self, id=None, from_date=None, to_date=None, date_type=None):
        date_type = "" if date_type is None else date_type
        sql_query = text(
            f"SELECT * FROM (SELECT *, TRY_CONVERT(DATE, REPLACE(Date, '/', '-'), 111) AS ConvertedDate "
            f"FROM app.fitler_chart_data_by_date(:from_date, :to_date, :id, :date_type)) AS Subquery "
            "ORDER BY ConvertedDate ASC"
        )

        query_data = session.query(ChartData).from_statement(
            sql_query
        ).params(from_date=from_date, to_date=to_date, id=id, date_type=date_type).all()
        return query_data


    def get_chartId_by_id(self, id):
        query = text("SELECT * FROM [estdco].[app].[chart_IDs] WHERE [level4_id] = :id")
        query_result = session.query(ChartIDs).from_statement(query).params(id=id).one()
        return query_result
