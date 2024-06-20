from sqlalchemy import Column, Boolean, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class StockTableColumns(Base):
    __tablename__ = 'stock_table_columns'
    __table_args__ = {'schema': 'web'}

    Username = Column(String(255), primary_key=True)
    Persian_symbol = Column(Boolean, nullable=True)
    Company_Name = Column(Boolean, nullable=True)
    Final_price = Column(Boolean, nullable=True)
    Yesterday_price = Column(Boolean, nullable=True)
    Industry_Group = Column(Boolean, nullable=True)
    Number_transactions = Column(Boolean, nullable=True)
    perc_last = Column(Boolean, nullable=True)
    perc_final = Column(Boolean, nullable=True)
    first_price = Column(Boolean, nullable=True)
    last_price = Column(Boolean, nullable=True)
    Value = Column(Boolean, nullable=True)
    market_cap = Column(Boolean, nullable=True)
    Vol = Column(Boolean, nullable=True)
    volume_ratio_to_month = Column(Boolean, nullable=True)
    entered_money = Column(Boolean, nullable=True)
    buy_per_capita = Column(Boolean, nullable=True)
    sell_per_capita = Column(Boolean, nullable=True)
    buyer_power = Column(Boolean, nullable=True)
    queue_value = Column(Boolean, nullable=True)
    status = Column(Boolean, nullable=True)
