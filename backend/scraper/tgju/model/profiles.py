from sqlalchemy import Column, Unicode
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Profiles(Base):
    __tablename__ = 'profiles'
    __table_args__ = {'schema': 'tgju'}

    Symbol = Column(Unicode(50), primary_key=True)
    NameEn = Column(Unicode(500))
    NameFa = Column(Unicode(500))
