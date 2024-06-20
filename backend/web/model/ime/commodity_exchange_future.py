from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper

Base = declarative_base()


class CommodityExchangeFuture(Base):
    __tablename__ = 'commodity_exchange_future'

    ContractDay = Column(String(255), primary_key=True)
    ContractCode = Column(String(255), primary_key=True)
    ContractDescription = Column(String(255), primary_key=True)
    TradesVolume = Column(String(255), primary_key=True)
    TradesValue = Column(String(255), primary_key=True)
    MinPrice = Column(String(255), primary_key=True)
    MaxPrice = Column(String(255), primary_key=True)
    LastPrice = Column(String(255), primary_key=True)
    FirstPrice = Column(String(255), primary_key=True)
    OpenInterest = Column(String(255), primary_key=True)
    ChangeOpenInterest = Column(String(255), primary_key=True)
    ActiveCustomers = Column(String(255), primary_key=True)
    ActiveBrokers = Column(String(255), primary_key=True)
    C_Buy = Column(String(255), primary_key=True)
    C_Sell = Column(String(255), primary_key=True)
    Vol_Hoghooghi_Sell = Column(String(255), primary_key=True)
    Val_Hoghooghi_Sell = Column(String(255), primary_key=True)
    Vol_Haghighi_Buy = Column(String(255), primary_key=True)
    Val_Haghighi_Buy = Column(String(255), primary_key=True)
    Vol_Haghighi_Sell = Column(String(255), primary_key=True)
    Val_Haghighi_Sell = Column(String(255), primary_key=True)
    LastSettlementPrice = Column(String(255), primary_key=True)
    TodaySettlementPrice = Column(String(255), primary_key=True)
    SettlementPricePercent = Column(String(255), primary_key=True)
    DT = Column(String(255), primary_key=True)
    DeliveryDate = Column(String(255), primary_key=True)
    WeeklyOpenInterests = Column(String(255), primary_key=True)
    WeeklyOpenInterestsPercent = Column(String(255), primary_key=True)
    MonthlyOpenInterests = Column(String(255), primary_key=True)
    MonthlyOpenInterestsPercent = Column(String(255), primary_key=True)
    WeeklySettlementPrice = Column(String(255), primary_key=True)
    WeeklySettlementPricePercent = Column(String(255), primary_key=True)
    MonthlySettlementPrice = Column(String(255), primary_key=True)
    MonthlySettlementPricePercent = Column(String(255), primary_key=True)
    UniqueID = Column(String(255), primary_key=True)
    Vol_Hoghooghi_Buy = Column(String(255), primary_key=True)
    Val_Hoghooghi_Buy = Column(String(255), primary_key=True)

    def to_dict(self):
        """
        Convert the object to a dictionary, replacing "nan" values with empty strings.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            value = getattr(self, column.name)
            result[column.name] = "" if value == "nan" else value
        return result
