from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MsgByFlow(Base):
    __tablename__ = 'tse_msg_by_flow'

    tseMsgIdn = Column(Unicode(50), primary_key=True)
    dEven = Column(Unicode(50))
    hEven = Column(Unicode(50))
    tseTitle = Column(Unicode(500))
    tseDesc = Column(Unicode(4000))
    flow = Column(Unicode(50))
