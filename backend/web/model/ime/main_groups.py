from dataclasses import dataclass

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

@dataclass
class ImeMainGroups(Base):
    __tablename__ = 'ime.main_groups'

    code = Column(String, primary_key=True)
    Name = Column(String, primary_key=True)
