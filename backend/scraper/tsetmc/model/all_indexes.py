from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AllIndexes(Base):
    __tablename__ = 'tse_all_indexes'

    lVal30 = Column(Unicode(50), primary_key=True)
    marketName = Column(Unicode(50))
    insCode = Column(Unicode(50))
    dEven = Column(Unicode(50))
    hEven = Column(Unicode(50))
    xDrNivJIdx004 = Column(Unicode(50))
    xPhNivJIdx004 = Column(Unicode(50))
    xPbNivJIdx004 = Column(Unicode(50))
    xVarIdxJRfV = Column(Unicode(50))
    last = Column(Unicode(50))
    indexChange = Column(Unicode(50))
    c1 = Column(Unicode(50))
    c2 = Column(Unicode(50))
    c3 = Column(Unicode(50))
    c4 = Column(Unicode(50))
