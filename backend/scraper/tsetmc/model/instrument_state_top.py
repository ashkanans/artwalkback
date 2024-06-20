from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class InstrumentStateTop(Base):
    __tablename__ = 'tse_instrument_state_top'

    idn = Column(Unicode(50), primary_key=True)
    dEven = Column(Unicode(50))
    hEven = Column(Unicode(50))
    insCode = Column(Unicode(500))
    lVal18AFC = Column(Unicode(50))
    lVal30 = Column(Unicode(50))
    cEtaval = Column(Unicode(50))
    realHeven = Column(Unicode(50))
    underSupervision = Column(Unicode(50))
    cEtavalTitle = Column(Unicode(50))
