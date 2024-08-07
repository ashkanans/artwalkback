from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper

Base = declarative_base()


class CommodityExchangeGold(Base):
    __tablename__ = 'commodity_exchange_gold'

    ContractID = Column(String(255), primary_key=True)
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
    ROW = Column(String(255), primary_key=True)
    Vol_Hoghooghi_Buy = Column(String(255), primary_key=True)
    Val_Hoghooghi_Buy = Column(String(255), primary_key=True)
    PersianDate = Column(String(255), primary_key=True)

    def to_dict(self):
        """
        Convert the object to a dictionary, replacing "nan" values with empty strings.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            value = getattr(self, column.name)
            result[column.name] = "" if value == "nan" else value
            if column.name in ["item.PersianDate", "item.FirstPrice", "item.LastPrice", "item.TradesVolume",
                               "item.MinPrice",
                               "item.MaxPrice", "item.LastPrice", "item.TradesValue"]:
                # Try casting the value to float, if it fails, keep it as is
                try:
                    value = float(value)
                except (TypeError, ValueError):
                    pass
            result[column.name] = value
        return result
