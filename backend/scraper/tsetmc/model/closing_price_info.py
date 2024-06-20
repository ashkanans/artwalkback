from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ClosingPriceInfo(Base):
    __tablename__ = "tse_closing_price_info"

    insCode = Column(Unicode(50), primary_key=True)

    instrument = Column(Unicode(50))
    lastHEven = Column(Unicode(50))
    finalLastDate = Column(Unicode(50))
    nvt = Column(Unicode(50))
    mop = Column(Unicode(50))
    pRedTran = Column(Unicode(50))
    thirtyDayClosingHistory = Column(Unicode(50))
    priceChange = Column(Unicode(50))
    priceMin = Column(Unicode(50))
    priceMax = Column(Unicode(50))
    priceYesterday = Column(Unicode(50))
    priceFirst = Column(Unicode(50))
    last = Column(Unicode(50))
    id = Column(Unicode(50))
    dEven = Column(Unicode(50))
    hEven = Column(Unicode(50))
    pClosing = Column(Unicode(50))
    iClose = Column(Unicode(50))
    yClose = Column(Unicode(50))
    pDrCotVal = Column(Unicode(50))
    zTotTran = Column(Unicode(50))
    qTotTran5J = Column(Unicode(50))
    qTotCap = Column(Unicode(50))
