from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Sources(Base):
    __tablename__ = 'sources'

    code = Column(String, primary_key=True, nullable=False)
    Name = Column(String, primary_key=True)
    TableNameMap = Column(String, primary_key=True)
