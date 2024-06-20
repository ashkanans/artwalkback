from sqlalchemy import Column, Unicode, Double, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TgjuCurrentProfiles(Base):
    __tablename__ = "current_profiles"
    __table_args__ = {'schema': 'tgju'}

    Symbol = Column(Unicode(50), primary_key=True)
    p = Column(Double(50))
    h = Column(Double(50))
    l = Column(Double(50))
    d = Column(Double(50))
    dp = Column(Double(50))
    dt = Column(Unicode(50))
    t = Column(Unicode(50))
    t_en = Column(Unicode(50))
    t_g = Column(Unicode(50))
    ts = Column(DateTime)
