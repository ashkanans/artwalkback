from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import class_mapper

Base = declarative_base()


class StockInfo(Base):
    __tablename__ = 'stocks_info'
    __table_args__ = {'schema': 'app'}

    Company_Name = Column(String(255), primary_key=True)
    tse_id = Column(String(255), primary_key=True)
    Persian_Symbol = Column(String(255), primary_key=True)
    Industry_Group = Column(String(255), primary_key=True)
    perc_final = Column(String(255), primary_key=True)
    perc_last = Column(String(255), primary_key=True)
    Value = Column(String(255), primary_key=True)
    Vol = Column(String(255), primary_key=True)
    market_cap = Column(String(255), primary_key=True)
    Final_price = Column(String(255), primary_key=True)
    first_price = Column(String(255), primary_key=True)
    last_price = Column(String(255), primary_key=True)
    Yesterday_price = Column(String(255), primary_key=True)
    Number_transactions = Column(String(255), primary_key=True)
    volume_ratio_to_month = Column(String(255), primary_key=True)
    buy_per_capita = Column(String(255), primary_key=True)
    sell_per_capita = Column(String(255), primary_key=True)
    entered_money = Column(String(255), primary_key=True)
    buyer_power = Column(String(255), primary_key=True)
    status = Column(String(255), primary_key=True)
    queue_value = Column(String(255), primary_key=True)


    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            result[column.name] = getattr(self, column.name)
        return result