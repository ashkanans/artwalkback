from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CommodityExchangeBazareMali(Base):
    __tablename__ = 'commodity_exchange_bazare_mali'

    id = Column(Integer, primary_key=True)
    Namad = Column(String(255), primary_key=True)
    LVal18AFC = Column(String(255), primary_key=True)
    DT = Column(String(255), primary_key=True)
    NamadDescription = Column(String(255), primary_key=True)
    PClosing = Column(String(255), primary_key=True)
    PDrCotVal = Column(String(255), primary_key=True)
    ZTotTran = Column(String(255), primary_key=True)
    QTotTran5J = Column(String(255), primary_key=True)
    QTotCap = Column(String(255), primary_key=True)
    PriceMin = Column(String(255), primary_key=True)
    PriceMax = Column(String(255), primary_key=True)
    PriceYesterday = Column(String(255), primary_key=True)
    LastTradeChangePrice = Column(String(255), primary_key=True)
    LastTradeChangePricePercent = Column(String(255), primary_key=True)
    LastPriceChangePrice = Column(String(255), primary_key=True)
    LastPriceChangePricePercent = Column(String(255), primary_key=True)
    DT_En = Column(String(255), primary_key=True)
    UniqueID = Column(String(255), primary_key=True)

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            # Check if the column is one of the columns to be cast to float
            if column.name in ["LastTradeChangePrice", "LastTradeChangePricePercent",
                               "LastPriceChangePrice", "LastPriceChangePricePercent"]:
                # Try casting the value to float, if it fails, keep it as is
                try:
                    value = float(value)
                except (TypeError, ValueError):
                    pass
            result[column.name] = value
        return result
