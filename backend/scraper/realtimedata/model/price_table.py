from sqlalchemy import Column, Float, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PriceTable(Base):
    """
    Represents a table with columns for exchange rates.
    """
    __tablename__ = 'real_time_price_table'

    currency_name = Column(Unicode(50), primary_key=True)  # نرخ ها
    unit = Column(Unicode(50))  # واحد
    year_1400 = Column(Float)  # 1400
    year_1401 = Column(Float)  # 1401
    year_1402 = Column(Float)  # 1402
    daily_price = Column(Float)  # قیمت روز

    def __repr__(self):
        return f"<PriceTable(id={self.id}, currency_name='{self.currency_name}', unit='{self.unit}', " \
               f"year_1400={self.year_1400}, year_1401={self.year_1401}, year_1402={self.year_1402}, " \
               f"daily_price={self.daily_price})>"
