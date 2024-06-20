from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GetRelatedCompany(Base):
    __tablename__ = 'tse_related_company'

    insCode = Column(Unicode(50), primary_key=True)
    cValMne = Column(Unicode(50))
    lVal18 = Column(Unicode(50))
    cSocCSAC = Column(Unicode(50))
    lSoc30 = Column(Unicode(50))
    yMarNSC = Column(Unicode(50))
    yVal = Column(Unicode(50))
    lVal30 = Column(Unicode(50))
    lVal18AFC = Column(Unicode(50))
    flow = Column(Unicode(50))
    cIsin = Column(Unicode(50))
    zTitad = Column(Unicode(50))
    baseVol = Column(Unicode(50))
    instrumentID = Column(Unicode(50))
    cgrValCot = Column(Unicode(50))
    cComVal = Column(Unicode(50))
    lastDate = Column(Unicode(50))
    sourceID = Column(Unicode(50))
    flowTitle = Column(Unicode(50))
    cgrValCotTitle = Column(Unicode(50))
