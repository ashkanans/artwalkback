from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TseIndustryIndexes(Base):
    __tablename__ = 'tse_industry_indexes'

    # 78 columns of type Unicode(4000)

    A = Column(Unicode(4000), primary_key=True)
    B = Column(Unicode(4000))
    C = Column(Unicode(4000))
    D = Column(Unicode(4000))

    def __init__(self, data):
        for i, value in enumerate(data):
            if i <= 26:
                column_name = chr(65 + (i))
            else:
                first_letter = chr(65 + ((i) // 26 - 1))
                second_letter = chr(65 + ((i) % 26))
                column_name = f"{first_letter}{second_letter}"
            setattr(self, column_name, value)
