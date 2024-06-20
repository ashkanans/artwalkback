from sqlalchemy import Column, Sequence, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Index(Base):
    """
    Represents the 'index' table in the database.
    """
    __tablename__ = 'fipiran_indexes'

    id = Column(Unicode(50), Sequence('Seq_fipiran_indexes'), primary_key=True)
    intId = Column(Unicode(50))
    nameFa = Column(Unicode(50))
    instrumentID = Column(Unicode(50))
    value = Column(Unicode(50))
    dateissue = Column(Unicode(50))
    gregorian_date = Column(Unicode(50))
    solar_date = Column(Unicode(50))
    code = Column(Unicode(50))
