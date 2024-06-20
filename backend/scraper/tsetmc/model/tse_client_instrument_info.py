from sqlalchemy import Column, Unicode, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper, ColumnProperty

Base = declarative_base()


class TseClientInstrumentInfo(Base):
    __tablename__ = 'tse_client_instrument_info'

    # Primary Key
    insCode = Column(Unicode(50), primary_key=True)
    instrumentID = Column(Unicode(50))
    latinSymbol = Column(Unicode(50))
    latinName = Column(Unicode(50))
    companyCode = Column(Unicode(50))
    symbol = Column(Unicode(50))
    name = Column(Unicode(50))
    cIsin = Column(Unicode(50))
    dEven = Column(Integer)
    flow = Column(Integer)
    lSoc30 = Column(Unicode(50))
    cGdSVal = Column(Unicode(50))
    cGrValCot = Column(Unicode(50))
    yMarNSC = Column(Unicode(50))
    cComVal = Column(Unicode(50))
    cSecVal = Column(Unicode(50))
    cSoSecVal = Column(Unicode(50))
    yVal = Column(Unicode(50))


    def __init__(self, insCode=None, instrumentID=None, latinSymbol=None, latinName=None, companyCode=None, symbol=None, name=None,
                 cIsin=None, dEven=None, flow=None,
                 lSoc30=None, cGdSVal=None, cGrValCot=None, yMarNSC=None, cComVal=None, cSecVal=None, cSoSecVal=None, yVal=None):
        self.insCode = insCode
        self.instrumentID = instrumentID
        self.latinSymbol = latinSymbol
        self.latinName = latinName
        self.companyCode = companyCode
        self.symbol = symbol
        self.name = name
        self.cIsin = cIsin
        self.dEven = dEven
        self.flow = flow
        self.lSoc30 = lSoc30
        self.cGdSVal = cGdSVal
        self.cGrValCot = cGrValCot
        self.yMarNSC = yMarNSC
        self.cComVal = cComVal
        self.cSecVal = cSecVal
        self.cSoSecVal = cSoSecVal
        self.yVal = yVal
