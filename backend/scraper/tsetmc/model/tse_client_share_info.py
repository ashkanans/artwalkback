from sqlalchemy import Column, Unicode, Integer, BigInteger, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper, ColumnProperty

Base = declarative_base()


class TseClientShareInfo(Base):
    __tablename__ = 'tse_client_share_info'

    idn = Column(BigInteger, primary_key=True)
    insCode = Column(BigInteger)
    dEven = Column(Integer)
    numberOfShareNew = Column(Float)
    NumberOfShareOld = Column(Float)

    def __init__(self, Idn=None, InsCode=None, DEven=None, NumberOfShareNew=None, NumberOfShareOld=None):
        self.idn = Idn
        self.insCode = InsCode
        self.dEven = DEven
        self.numberOfShareNew = NumberOfShareNew
        self.NumberOfShareOld = NumberOfShareOld

    @classmethod
    def from_row(cls, row):
        return cls(
            Idn=int(row[0]),
            InsCode=int(row[1]),
            DEven=int(row[2]),
            NumberOfShareNew=float(row[3]),
            NumberOfShareOld=float(row[4])
        )
