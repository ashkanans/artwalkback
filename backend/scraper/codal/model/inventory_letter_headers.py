
from sqlalchemy import Column, Integer, BigInteger, Sequence, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class InventoryLetterHeaders(Base):
    __tablename__ = 'codal_inventory_letter_headers'

    id = Column(Unicode(50), primary_key=True)
    type = Column(Unicode(50))
    symbol = Column(Unicode(50))
