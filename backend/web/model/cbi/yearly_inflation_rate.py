from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class InflationRate(Base):
    __tablename__ = 'inflation_rate'
    month = Column(String(255), nullable=True, primary_key=True)
    type = Column(String(255), nullable=True, primary_key=True)
    price_index = Column(String(255), nullable=True, primary_key=True)
    Inflation = Column(String(255), nullable=True, primary_key=True)
    year = Column(String(255), nullable=True, primary_key=True)
