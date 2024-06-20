from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper

Base = declarative_base()


class CommodityExchangeMonaghesat(Base):
    __tablename__ = 'commodity_exchange_monaghesat'

    Id = Column(String(255), primary_key=True)
    ArzehPk = Column(String(255), primary_key=True)
    RingName = Column(String(255), primary_key=True)
    GoodsName = Column(String(255), primary_key=True)
    Symbol = Column(String(255), primary_key=True)
    ProducerName = Column(String(255), primary_key=True)
    Supplier = Column(String(255), primary_key=True)
    ContractType = Column(String(255), primary_key=True)
    TradeDate_Jalali = Column(String(255), primary_key=True)
    DeliveryDate_Jalali = Column(String(255), primary_key=True)
    BasePrice = Column(String(255), primary_key=True)
    MinPrice = Column(String(255), primary_key=True)
    MaxPrice = Column(String(255), primary_key=True)
    FinalPrice = Column(String(255), primary_key=True)
    TradeValue = Column(String(255), primary_key=True)
    OfferVolume = Column(String(255), primary_key=True)
    DemandVolume = Column(String(255), primary_key=True)
    TradeVolume = Column(String(255), primary_key=True)
    OfferMinPrice = Column(String(255), primary_key=True)
    DemandMaxPrice = Column(String(255), primary_key=True)
    Floor = Column(String(255), primary_key=True)
    Comment = Column(String(255), primary_key=True)
    DeliveryPoint = Column(String(255), primary_key=True)
    Currency = Column(String(255), primary_key=True)
    Unit = Column(String(255), primary_key=True)
    cBrokerSpcName = Column(String(255), primary_key=True)
    ModeDescription = Column(String(255), primary_key=True)
    MethodDescription = Column(String(255), primary_key=True)

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            result[column.name] = getattr(self, column.name)
        return result
