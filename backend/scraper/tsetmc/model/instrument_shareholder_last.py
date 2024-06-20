from datetime import datetime

from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper, ColumnProperty

Base = declarative_base()


class InstrumentShareholderLast(Base):
    __tablename__ = "None"

    # Primary Key
    shareholderShareID = Column(Unicode(50), primary_key=True)

    # General Information
    datetime_str = Column(Unicode(50), primary_key=True)
    shareholderID = Column(Unicode(50))
    shareholderName = Column(Unicode(50))
    cIsin = Column(Unicode(50))
    dEven = Column(Unicode(50))
    numberOfShares = Column(Unicode(50))
    perOfShares = Column(Unicode(50))
    change = Column(Unicode(50))
    changeAmount = Column(Unicode(50))

    columns = [
        'shareholderID',
        'shareholderName',
        'cIsin',
        'dEven',
        'numberOfShares',
        'perOfShares',
        'change',
        'changeAmount',
        'shareholderShareID'
    ]

    @classmethod
    def list_of_objects_to_dict_list(cls, object_list):
        """
        Convert a list of ClosingPriceDailyList objects to a list of dictionaries.

        Args:
        - object_list (list): List of ClosingPriceDailyList objects.

        Returns:
        - list: List of dictionaries where keys are column names and values are object fields.
        """
        if not object_list:
            return []

        # Get column names from the class mapper
        column_names = [prop.key for prop in class_mapper(cls).iterate_properties
                        if isinstance(prop, ColumnProperty)]

        # Create a list of dictionaries
        dict_list = [dict((col, getattr(obj, col)) for col in column_names) for obj in object_list]

        return dict_list

    @classmethod
    def list_of_dicts_to_object_list(cls, dict_list):
        """
        Convert a list of dictionaries to a list of ClosingPriceDailyList objects.

        Args:
        - dict_list (list): List of dictionaries where keys are column names and values are object fields.

        Returns:
        - list: List of ClosingPriceDailyList objects.
        """
        if not dict_list:
            return []

        # Create a list of ClosingPriceDailyList objects
        object_list = [cls(**data) for data in dict_list]

        return object_list

    def create_instrument_shareholder_last(self, instrument_shareholder_last_objects):
        shareholder_history = []

        for element in instrument_shareholder_last_objects:

            
            shareholderID = element.shareholderID
            shareholderName = element.shareholderName
            cIsin = element.cIsin
            dEven = element.dEven
            numberOfShares = element.numberOfShares
            perOfShares = element.perOfShares
            change = element.change
            changeAmount = element.changeAmount
            shareholderShareID = element.shareholderShareID
            time = element.datetime_str
            
            shareholder_history.append((shareholderID,
                shareholderName,
                cIsin,
                dEven,
                numberOfShares,
                perOfShares,
                change,
                changeAmount,
                shareholderShareID,
                time
            ))

        shareholder_history.sort(key=lambda x: datetime.strptime(x[-1], "%Y-%m-%d_%H-%M-%S"))

        return shareholder_history
