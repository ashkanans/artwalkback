from sqlalchemy import Column, Unicode, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class InstrumentGroup(Base):
    """
    Represents the 'instrumentgroups' table in the database.
    """
    __tablename__ = 'instrument_groups'
    __table_args__ = {'schema': 'tsetmc'}

    id = Column(Integer, primary_key=True)
    code = Column(Integer)
    type = Column(Unicode(50))
    name = Column(Unicode(50))
    description = Column(Unicode(50))
