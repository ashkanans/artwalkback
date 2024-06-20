from sqlalchemy import Column, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper

Base = declarative_base()


class CommodityExchangePhysical(Base):
    __tablename__ = 'commodity_exchange_physical'

    GoodsName = Column(String, primary_key=True)
    Symbol = Column(String, primary_key=True)
    ProducerName = Column(String, primary_key=True)
    ContractType = Column(String, primary_key=True)
    MinPrice = Column(String, primary_key=True)
    Price = Column(String, primary_key=True)
    MaxPrice = Column(String, primary_key=True)
    arze = Column(Float, primary_key=True)
    ArzeBasePrice = Column(Float, primary_key=True)
    arzeMinPrice = Column(Float, primary_key=True)
    taghaza = Column(Float, primary_key=True)
    taghazavoroudi = Column(Float, primary_key=True)
    taghazaMaxPrice = Column(Float, primary_key=True)
    Quantity = Column(Float, primary_key=True)
    TotalPrice = Column(Float, primary_key=True)
    date = Column(String, primary_key=True)
    DeliveryDate = Column(String, primary_key=True)
    Warehouse = Column(String, primary_key=True)
    ArzehKonandeh = Column(String, primary_key=True)
    SettlementDate = Column(String, primary_key=True)
    Category = Column(String, primary_key=True)
    xTalarReportPK = Column(String, primary_key=True)
    bArzehRadifTarSarresid = Column(String, primary_key=True)
    cBrokerSpcName = Column(String, primary_key=True)
    ModeDescription = Column(String, primary_key=True)
    MethodDescription = Column(String, primary_key=True)
    MinPrice1 = Column(String, primary_key=True)
    Price1 = Column(String, primary_key=True)
    Currency = Column(String, primary_key=True)
    arzehPk = Column(String, primary_key=True)
    # Unit_Arr_0 = Column(String, primary_key=True)
    UNIC_CODE = Column(String, primary_key=True)

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            result[column.name] = getattr(self, column.name)
        return result
