from sqlalchemy import Column, Unicode, Float, DateTime, func, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ClosingPriceInfoAdjusted(Base):
    __tablename__ = "tse_closing_price_info_adjusted"

    insCode = Column(Unicode(50), primary_key=True)
    dEven = Column(Integer, primary_key=True)
    createdDate = Column(DateTime(timezone=True), server_default=func.now())
    updatedDate = Column(DateTime(timezone=True), onupdate=func.now())
    pClosing = Column(Float)
    pDrCotVal = Column(Float)
    priceMin = Column(Float)
    priceMax = Column(Float)
    priceYesterday = Column(Float)
    priceFirst = Column(Float)
    adjustMode = Column(Integer, primary_key=True)
    qTotCap = Column(Float)
    qTotTran5J = Column(Float)
    zTotTran = Column(Float)
    def __init__(self, insCode=None, dEven=None, pclosing=None, pdrCotVal=None, priceMin=None, priceMax=None ,priceYesterday=None,
                 priceFirst=None, adjustMode=None, qTotCap=None, qTotTran5J=None, zTotTran=None):
        self.insCode = insCode
        self.dEven = dEven
        self.pClosing = pclosing
        self.pdrCotVal = pdrCotVal
        self.priceMin = priceMin
        self.priceMax = priceMax
        self.priceYesterday = priceYesterday
        self.priceFirst = priceFirst
        self.adjustMode = adjustMode
        self.qTotCap = qTotCap
        self.qTotTran5J = qTotTran5J
        self.zTotTran = zTotTran

