from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class IndexesId(Base):

     __tablename__ = 'fipiran_indexes_id'

     InstrumentID = Column(Unicode(50), primary_key=True)
     LVal30 = Column(Unicode(50))
     IntId = Column(Unicode(50))
     NameFa = Column(Unicode(50))
