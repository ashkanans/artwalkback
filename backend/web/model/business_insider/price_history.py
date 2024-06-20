from sqlalchemy import Column, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def bi_data_list_to_dict(objects_list):
    result = []

    for item in objects_list:
        temp_dict = {"open": float(item.open.replace(",", "")), "low": float(item.low.replace(",", "")),
                     "max": float(item.max.replace(",", "")), "close": float(item.close.replace(",", "")),
                     "Date": item.Date}
        result.append(temp_dict)

    return result


class PriceHistory(Base):
    __tablename__ = 'price_history'

    ID = Column(Float, nullable=True, primary_key=True)
    open = Column(String(255), nullable=True, primary_key=True)
    low = Column(String(255), nullable=True, primary_key=True)
    max = Column(String(255), primary_key=True, nullable=True)
    close = Column(String(255), primary_key=True, nullable=True)
    Date = Column(String(255), primary_key=True, nullable=True)
