from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper

Base = declarative_base()


class CommodityExchangePremium(Base):
    __tablename__ = 'commodity_exchange_premium'

    GoodsName = Column(String(255), primary_key=True)
    Symbol = Column(String(255), primary_key=True)
    ProducerName = Column(String(255), primary_key=True)
    ContractType = Column(String(255), primary_key=True)
    MinPrice = Column(String(255), primary_key=True)
    Price = Column(String(255), primary_key=True)
    MaxPrice = Column(String(255), primary_key=True)
    arze = Column(String(255), primary_key=True)
    ArzeBasePrice = Column(String(255), primary_key=True)
    arzeMinPrice = Column(String(255), primary_key=True)
    taghaza = Column(String(255), primary_key=True)
    taghazavoroudi = Column(String(255), primary_key=True)
    taghazaMaxPrice = Column(String(255), primary_key=True)
    Quantity = Column(String(255), primary_key=True)
    TotalPrice = Column(String(255), primary_key=True)
    date = Column(String(255), primary_key=True)
    DeliveryDate = Column(String(255), primary_key=True)
    Warehouse = Column(String(255), primary_key=True)
    ArzehKonandeh = Column(String(255), primary_key=True)
    SettlementDate = Column(String(255), primary_key=True)
    Category = Column(String(255), primary_key=True)
    xTalarReportPK = Column(String(255), primary_key=True)
    bArzehRadifTarSarresid = Column(String(255), primary_key=True)
    cBrokerSpcName = Column(String(255), primary_key=True)
    ModeDescription = Column(String(255), primary_key=True)
    MethodDescription = Column(String(255), primary_key=True)
    MinPrice1 = Column(String(255), primary_key=True)
    Price1 = Column(String(255), primary_key=True)
    Currency = Column(String(255), primary_key=True)
    Unit = Column(String(255), primary_key=True)
    arzehPk = Column(String(255), primary_key=True)
    Talar = Column(String(255), primary_key=True)
    PacketName = Column(String(255), primary_key=True)
    Tasvieh = Column(String(255), primary_key=True)

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            result[column.name] = getattr(self, column.name)
        return result
