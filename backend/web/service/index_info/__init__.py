from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.tsetmc.index_info import IndexInfo
from backend.web.service.sort_config import SortConfig

engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class IndexInfoService:
    def __init__(self):
        self.sortConfig = SortConfig()
        self.query_result: list = []
        pass

    def get_all_index_info(self, sort_by: str, sort_order: str) -> list[IndexInfo]:
        config_query = SortConfig().get_config_query(sort_order=sort_order, sort_by=sort_by, model=IndexInfo)
        try:
            self.query_result = session.query(IndexInfo).from_statement(
                text(f"SELECT * FROM app.index_info {config_query}")
            ).all()
        finally:
            session.close()
        return self.query_result
