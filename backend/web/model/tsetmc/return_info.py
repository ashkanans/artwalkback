from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ReturnInfo(Base):
    __tablename__ = 'return_info'

    tse_id = Column(Integer, primary_key=True)
    return_value = Column(Float, primary_key=True)
    symbol = Column(String(255), primary_key=True)
    type = Column(String(255), primary_key=True)
    index_type = Column(String(255), primary_key=True)
    rank = Column(Integer, primary_key=True)
