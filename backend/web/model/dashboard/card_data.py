from sqlalchemy import Column, NVARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper

Base = declarative_base()


class CardData(Base):
    __tablename__ = 'card_data'

    idName = Column(NVARCHAR(500), primary_key=True)
    value = Column(NVARCHAR(500), primary_key=True)

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            result[column.name] = getattr(self, column.name)
        return result

    def to_list(self, card_data_list):
        """
        Convert a list of CardData objects to two separate lists of idNames and values.
        """
        idNames = []
        values = []

        for card_data in card_data_list:
            idNames.append(card_data.idName)
            values.append(card_data.value)

        return idNames, values
