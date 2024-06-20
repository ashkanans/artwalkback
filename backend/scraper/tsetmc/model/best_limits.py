from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper, ColumnProperty

Base = declarative_base()


class BestLimits(Base):
    __tablename__ = "tse_best_limits"

    key = Column(Unicode(50), primary_key=True)
    insCode = Column(Unicode(50))
    number = Column(Unicode(50))
    qTitMeDem = Column(Unicode(50))
    zOrdMeDem = Column(Unicode(50))
    pMeDem = Column(Unicode(50))
    pMeOf = Column(Unicode(50))
    zOrdMeOf = Column(Unicode(50))
    qTitMeOf = Column(Unicode(50))
