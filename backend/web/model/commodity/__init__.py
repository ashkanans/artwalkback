from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass

Base = declarative_base()


@dataclass
class CommodityModel(Base):
    __tablename__ = 'businessinsider.ID'

    category = Column(String, primary_key=True)
    Name_en = Column(String, primary_key=True)
    Unit = Column(String, primary_key=True)
    ID = Column(Integer, primary_key=True)
    Name_fa = Column(String, primary_key=True)
    category_fa = Column(String, primary_key=True)

    def serialize(self):
        return {"category": self.category,
                "Name_en": self.Name_en,
                "Unit": self.Unit,
                "ID": self.ID,
                "Name_fa": self.Name_fa,
                "category_fa": self.category_fa
                }
