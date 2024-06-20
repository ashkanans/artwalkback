from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import class_mapper
Base = declarative_base()


class ImportantFilters(Base):
    __tablename__ = 'Important_filters'
    __table_args__ = {'schema': 'app'}
    tse_id_2 = Column(String(255), nullable=True, primary_key=True)
    Persian_symbol = Column(String(255), nullable=True, primary_key=True)
    first_price = Column(String(255), nullable=True, primary_key=True)
    Final_price = Column(String(255), nullable=True, primary_key=True)
    last_price = Column(String(255), nullable=True, primary_key=True)
    Number_transactions = Column(String(255), nullable=True, primary_key=True)
    Vol = Column(String(255), nullable=True, primary_key=True)
    Value = Column(String(255), nullable=True, primary_key=True)
    Yesterday_price = Column(String(255), nullable=True, primary_key=True)
    per_change_price = Column(String(255), nullable=True, primary_key=True)
    status = Column(String(255), nullable=True, primary_key=True)
    queue_value = Column(String(255), nullable=True, primary_key=True)
    perc_last = Column(String(255), nullable=True, primary_key=True)
    volume_ratio_to_month = Column(String(255), nullable=True, primary_key=True)
    buy_per_capita = Column(String(255), nullable=True, primary_key=True)
    sell_per_capita = Column(String(255), nullable=True, primary_key=True)
    entered_money = Column(String(255), nullable=True, primary_key=True)
    buyer_power = Column(String(255), nullable=True, primary_key=True)


    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            result[column.name] = getattr(self, column.name)
        return result
