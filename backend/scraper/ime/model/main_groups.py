from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MainGroups(Base):
    __tablename__ = "ime_main_groups"
    code = Column(Unicode(50), primary_key=True)
    Name = Column(Unicode(50))
