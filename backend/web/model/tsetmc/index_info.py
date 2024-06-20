from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import class_mapper

Base = declarative_base()


class IndexInfo(Base):
    __tablename__ = 'index_info'
    __table_args__ = {'schema': 'app'}
    tse_id = Column(String(255), nullable=True, primary_key=True)
    return_value = Column(String(255), nullable=True, primary_key=True)
    index_name = Column(String(255), nullable=True, primary_key=True)
    type = Column(String(255), nullable=True, primary_key=True)
    index_type = Column(String(255), nullable=True, primary_key=True)
    rank = Column(String(255), nullable=True, primary_key=True)

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            result[column.name] = getattr(self, column.name)
        return result
