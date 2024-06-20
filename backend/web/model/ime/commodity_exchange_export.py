from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper

Base = declarative_base()


class CommodityExchangeExport(Base):
    __tablename__ = 'commodity_exchange_export'

    cBrokerSpcName = Column(String, primary_key=True)
    ID = Column(Integer, primary_key=True)
    GoodsName = Column(String, primary_key=True)
    Symbol = Column(String, primary_key=True)
    ProducerName = Column(String, primary_key=True)
    ContractType = Column(String, primary_key=True)
    DeliveryDate = Column(String, primary_key=True)
    MinPrice = Column(Float, primary_key=True)
    Price = Column(Float, primary_key=True)
    MaxPrice = Column(Float, primary_key=True)
    arze = Column(Float, primary_key=True)
    BasePrice = Column(Float, primary_key=True)
    arzeMinPrice = Column(Float, primary_key=True)
    taghaza = Column(Float, primary_key=True)
    taghazaMaxPrice = Column(Float, primary_key=True)
    Quantity = Column(Float, primary_key=True)
    TotalPrice = Column(Float, primary_key=True)
    BasketDetail = Column(String, primary_key=True)
    GroupName = Column(String, primary_key=True)
    SubGroupName = Column(String, primary_key=True)
    Warehouse = Column(String, primary_key=True)
    date = Column(String, primary_key=True)
    typeName = Column(String, primary_key=True)
    TaghazaVoroudi = Column(Float, primary_key=True)
    ArzeBasePrice = Column(Float, primary_key=True)
    ArzehKonandeh = Column(String, primary_key=True)
    bArzehRadifTarSarresid = Column(String, primary_key=True)
    xKala_xGrouhAsliKalaPK = Column(Integer, primary_key=True)
    xKala_xGrouhKalaPK = Column(Integer, primary_key=True)
    xKala_xZirGrouhKalaPK = Column(Integer, primary_key=True)
    xNamad_xTolidKonandehPK = Column(Integer, primary_key=True)
    xRingPK = Column(Integer, primary_key=True)
    xRingName = Column(String, primary_key=True)
    ModeDescription = Column(String, primary_key=True)
    MethodDescription = Column(String, primary_key=True)
    NerkhArz = Column(Float, primary_key=True)
    Currency = Column(String, primary_key=True)
    Unit = Column(String, primary_key=True)
    arzehPk = Column(String, primary_key=True)
    Talar = Column(String, primary_key=True)

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            result[column.name] = getattr(self, column.name)
        return result
