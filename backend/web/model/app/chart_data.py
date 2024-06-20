from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def data_list_to_dict(objects_list):
    result = []

    for item in objects_list:
        temp_dict = {
            "dateGr": item.date,
            "dateSh": item.DateSh,
            "open": item.open,
            "low": item.low,
            "high": item.high,
            "close": item.close
        }
        result.append(temp_dict)

    return result


class ChartData(Base):
    __tablename__ = 'chart_data'
    __table_args__ = {'schema': 'app'}

    open = Column(Float, primary_key=True, nullable=True)
    close = Column(Float, primary_key=True, nullable=True)
    high = Column(Float, primary_key=True, nullable=True)
    low = Column(Float, primary_key=True, nullable=True)
    volume = Column(Integer, primary_key=True, nullable=True)
    level4_id = Column(String(255), primary_key=True, nullable=True)
    date = Column(String(255), primary_key=True, nullable=True)
    DateSh = Column(String(255), primary_key=True, nullable=True)
    prKey = Column(String(255), primary_key=True, nullable=True)

    def __init__(self, open=None, close=None, high=None, low=None, volume=None, level4_id=None, date=None):
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.volume = volume
        self.level4_id = level4_id
        self.date = date
