from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CombinedDropdownData(Base):
    __tablename__ = 'combined_dropdown_data'

    code = Column(String, primary_key=True)
    Name = Column(String, primary_key=True)
    TableName = Column(String, primary_key=True)
    TableNameMap = Column(String, primary_key=True)
