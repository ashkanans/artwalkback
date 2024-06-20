from sqlalchemy import Column, NVARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher_info'

    Symbol = Column(NVARCHAR(4000), primary_key=True)
    National_Code = Column(NVARCHAR(4000))

    @classmethod
    def get_publishers_mapping(cls, publishers):
        mapping_list = []
        for publisher in publishers:
            mapping_list.append({publisher.National_Code: publisher.Symbol})
        return mapping_list
