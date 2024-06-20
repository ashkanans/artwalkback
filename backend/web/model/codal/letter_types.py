from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LetterType(Base):
    __tablename__ = 'letter_types'

    name = Column(String(500), primary_key=True)
    reportTypes = Column(String(10), primary_key=True)
    persianCodes = Column(String(10), primary_key=True)
    letterNameExpression = Column(String(200), primary_key=True)
