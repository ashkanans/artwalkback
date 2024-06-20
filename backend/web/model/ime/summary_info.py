from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SummaryInfo(Base):
    __tablename__ = 'summary_info'

    measure = Column(String, primary_key=True)
    Day = Column(String, primary_key=True)
    Week = Column(String, primary_key=True)
    Month = Column(String, primary_key=True)
    Year = Column(String, primary_key=True)
