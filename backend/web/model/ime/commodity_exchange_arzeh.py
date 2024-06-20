from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper

Base = declarative_base()


class CommodityExchangeArzeh(Base):
    __tablename__ = 'commodity_exchange_arzeh'

    Attachment = Column(String, primary_key=True)
    bArzehRadifPK = Column(Integer, primary_key=True)
    cBrokerSpcName = Column(String, primary_key=True)
    bArzehTarArzeh = Column(String, primary_key=True)
    bArzehRadifNamadKala = Column(String, primary_key=True)
    bArzehRadifShekl = Column(String, primary_key=True)
    bArzehRadifSize = Column(String, primary_key=True)
    xTolidKonandehSharh = Column(String, primary_key=True)
    xMahalTahvilSharh = Column(String, primary_key=True)
    bArzehRadifArzeh = Column(Integer, primary_key=True)
    bArzehRadifMab = Column(Float, primary_key=True)
    xContractKindSharh = Column(String, primary_key=True)
    bArzehRadifTarTahvil = Column(String, primary_key=True)
    bArzehRadifArzehSharh = Column(String, primary_key=True)
    bArzehRadifMaxMahmooleh = Column(Integer, primary_key=True)
    bArzehRadifZaribMahmooleh = Column(Integer, primary_key=True)
    bArzehRadifMinMahmooleh = Column(Integer, primary_key=True)
    bArzehRadifSumBuyOrders = Column(String, primary_key=True)
    bArzehRadifStatusSharh = Column(String, primary_key=True)
    bArzehRadifMinMab = Column(Float, primary_key=True)
    bArzehRadifMaxMab = Column(String, primary_key=True)
    bArzehRadifDarsad = Column(Integer, primary_key=True)
    bArzehRadifMinArzeh = Column(Float, primary_key=True)
    bArzehRadifKashfNerkhMinBuy = Column(Float, primary_key=True)
    bArzehRadifMinTakhsis = Column(Integer, primary_key=True)
    bArzehRadifMojazTahvilMinTel = Column(String, primary_key=True)
    bArzehRadifVahedAndazegiri = Column(String, primary_key=True)
    bArzehRadifAndazehMahmuleh = Column(Integer, primary_key=True)
    bArzehRadifTasviehTypeID = Column(Integer, primary_key=True)
    bArzehRadifTasviehTypeSharh = Column(String, primary_key=True)
    bArzehRadifTikSize = Column(Float, primary_key=True)
    bArzehRadifArzehAvalieh = Column(Integer, primary_key=True)
    bArzehRadifMaxBasePrice = Column(String, primary_key=True)
    ArzehKonandeh = Column(String, primary_key=True)
    xKalaNamTejari = Column(String, primary_key=True)
    xKalaNamadKala = Column(String, primary_key=True)
    ArzeshArzeh = Column(String, primary_key=True)
    bArzehRadifMaxKharidM = Column(String, primary_key=True)
    bArzehRadifTedadMahmooleh = Column(Integer, primary_key=True)
    xTolidKonandehPK = Column(Integer, primary_key=True)
    xKala_xGrouhAsliKalaPK = Column(Integer, primary_key=True)
    xKala_xGrouhKalaPK = Column(Integer, primary_key=True)
    xKala_xZirGrouhKalaPK = Column(Integer, primary_key=True)
    bArzehRadifMode = Column(Integer, primary_key=True)
    bArzehRadifBuyMethod = Column(Integer, primary_key=True)
    ModeDescription = Column(String, primary_key=True)
    MethodDescription = Column(String, primary_key=True)
    Currency = Column(String, primary_key=True)
    Unit = Column(String, primary_key=True)
    id = Column(String, primary_key=True)
    Talar = Column(String, primary_key=True)

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            result[column.name] = getattr(self, column.name)
        return result
