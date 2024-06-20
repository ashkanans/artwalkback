from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass

Base = declarative_base()


@dataclass
class CommodityPriceHistory(Base):
    __tablename__ = 'businessinsider.price_history'

    Close = Column(String, primary_key=True)
    Date = Column(String, primary_key=True)
    unic_code = Column(String, primary_key=True)
    ID = Column(Integer, primary_key=True)


    def serialize(self):
        return {"Close": self.Close,
                "Date": self.Date,
                "unic_code": self.unic_code,
                "ID": self.ID,

                }
