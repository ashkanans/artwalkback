from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass

Base = declarative_base()


@dataclass
class IndexInfoModel(Base):
    __tablename__ = 'app.index_info'

    return_value = Column(String, primary_key=True)
    tse_id = Column(String, primary_key=True)
    index_name = Column(String, primary_key=True)
    type = Column(Integer, primary_key=True)
    index_type = Column(String, primary_key=True)
    rank = Column(String, primary_key=True)

    def serialize(self):
        return {"return_value": self.return_value,
                "tse_id": self.tse_id,
                "index_name": self.index_name,
                "type": self.type,
                "index_type": self.index_type,
                "rank": self.rank
                }
