from sqlalchemy import Column, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PriceArchive(Base):
    __tablename__ = 'price_archive'
    time = Column(DateTime, nullable=True, primary_key=True)
    price = Column(Float, nullable=True, primary_key=True)
    id = Column(String(255), nullable=True, primary_key=True)
    blend_name = Column(String(255), nullable=True, primary_key=True)
