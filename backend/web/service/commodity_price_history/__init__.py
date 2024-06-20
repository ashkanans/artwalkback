from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.commodity_price_history import CommodityPriceHistory

engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class CommodityPriceHistoryService:
    def __init__(self):
        pass

    def get_commodity_price_history(self, commodity_id):
        query_result = session.query(CommodityPriceHistory).from_statement(
            text("SELECT * FROM businessinsider.price_history WHERE ID=:commodity_id")
        ).params(commodity_id=commodity_id).all()
        return query_result
