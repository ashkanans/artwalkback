from dataclasses import dataclass

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

@dataclass
class ImeSubCategoryGroups(Base):
    __tablename__ = 'ime.sub_category_groups'

    code = Column(String, primary_key=True)
    Name = Column(String, primary_key=True)
