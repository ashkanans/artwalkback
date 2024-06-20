from dataclasses import dataclass

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

@dataclass
class ImeContractType(Base):
    __tablename__ = 'ime.contract_type'
    id = Column(Integer, primary_key=True)
    contractTypeFa = Column(String, primary_key=True)
    contractTypeEn = Column(String, primary_key=True)
