from sqlalchemy import Column, NVARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper

Base = declarative_base()


class ExportBarchart(Base):
    __tablename__ = 'export_barchart'

    idName = Column(NVARCHAR(500), primary_key=True)
    USD = Column(NVARCHAR(500), primary_key=True)
    USD_AZAD = Column(NVARCHAR(500), primary_key=True)
    IRR = Column(NVARCHAR(500), primary_key=True)
    IRR_Export = Column(NVARCHAR(500), primary_key=True)

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
        USD = []
        USD_AZAD = []
        IRR = []
        IRR_Export = []

        for card_data in card_data_list:
            idNames.append(card_data.idName)
            USD.append(card_data.USD)
            USD_AZAD.append(card_data.USD_AZAD)

            IRR.append(card_data.IRR)
            IRR_Export.append(card_data.IRR_Export)

        return idNames, USD, USD_AZAD, IRR, IRR_Export
