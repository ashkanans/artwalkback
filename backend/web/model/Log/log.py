import datetime
from sqlalchemy import Column, TIMESTAMP, VARCHAR, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Log(Base):
    __tablename__ = 'logger'

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.datetime.now())
    http_method = Column(VARCHAR(50))
    endpoint = Column(VARCHAR(50))
    client_ip = Column(VARCHAR(50))
