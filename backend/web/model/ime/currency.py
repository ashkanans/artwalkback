from dataclasses import dataclass

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


@dataclass
class ImeCurrency(Base):
    __tablename__ = 'ime.currency'
    id = Column(Integer, primary_key=True)
    currencyFa = Column(String, primary_key=True)
    currencyEn = Column(String, primary_key=True)
    acrynom = Column(String, primary_key=True)
