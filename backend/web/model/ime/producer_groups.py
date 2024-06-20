from dataclasses import dataclass

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

@dataclass
class ImeProducerGroups(Base):
    __tablename__ = 'ime.producer_groups'

    code = Column(String, primary_key=True)
    name = Column(String, primary_key=True)
