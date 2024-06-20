from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ClientType(Base):
    __tablename__ = "tse_client_type"

    insCode = Column(Unicode(50), primary_key=True)
    buy_I_Volume = Column(Unicode(50))
    buy_N_Volume = Column(Unicode(50))
    buy_DDD_Volume = Column(Unicode(50))
    buy_CountI = Column(Unicode(50))
    buy_CountN = Column(Unicode(50))
    buy_CountDDD = Column(Unicode(50))
    sell_I_Volume = Column(Unicode(50))
    sell_N_Volume = Column(Unicode(50))
    sell_CountI = Column(Unicode(50))
    sell_CountN = Column(Unicode(50))
