from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class EnteredMoneyRank(Base):
    __tablename__ = 'entered_money_rank'

    tse_id = Column(String(255), primary_key=True, nullable=True)
    type = Column(String(255), primary_key=True)
    entered_money = Column(Float, primary_key=True)
    rank = Column(Integer, primary_key=True)
    type_rank = Column(String(255), primary_key=True)
    Persian_symbol = Column(String(255), primary_key=True)
    type_report = Column(String(255), primary_key=True)
