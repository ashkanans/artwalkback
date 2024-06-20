from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GetTrade(Base):
    __tablename__ = 'tse_get_trade'

    id = Column(Unicode(50), primary_key=True)
    insCode = Column(Unicode(50))
    dEven = Column(Unicode(50))
    nTran = Column(Unicode(50))
    hEven = Column(Unicode(50))
    qTitTran = Column(Unicode(50))
    pTran = Column(Unicode(50))
    qTitNgJ = Column(Unicode(50))
    iSensVarP = Column(Unicode(50))
    pPhSeaCotJ = Column(Unicode(50))
    pPbSeaCotJ = Column(Unicode(50))
    iAnuTran = Column(Unicode(50))
    xqVarPJDrPRf = Column(Unicode(50))
    canceled = Column(Unicode(50))
