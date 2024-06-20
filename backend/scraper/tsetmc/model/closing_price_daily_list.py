from datetime import datetime

from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper, ColumnProperty

Base = declarative_base()


class ClosingPriceDailyList(Base):
    __tablename__ = "None"

    # Primary Key
    datetime_str = Column(Unicode(50), primary_key=True)

    # General Information
    priceChange = Column(Unicode(50))
    priceMin = Column(Unicode(50))
    priceMax = Column(Unicode(50))
    priceYesterday = Column(Unicode(50))
    priceFirst = Column(Unicode(50))
    last = Column(Unicode(50))
    id = Column(Unicode(50))
    insCode = Column(Unicode(50))
    dEven = Column(Unicode(50))
    hEven = Column(Unicode(50))
    pClosing = Column(Unicode(50))
    iClose = Column(Unicode(50))
    yClose = Column(Unicode(50))
    pDrCotVal = Column(Unicode(50))
    zTotTran = Column(Unicode(50))
    qTotTran5J = Column(Unicode(50))
    qTotCap = Column(Unicode(50))

    columns = [
        'datetime_str',
        'priceChange',
        'priceMin',
        'priceMax',
        'priceYesterday',
        'priceFirst',
        'last',
        'id',
        'insCode',
        'dEven',
        'hEven',
        'pClosing',
        'iClose',
        'yClose',
        'pDrCotVal',
        'zTotTran',
        'qTotTran5J',
        'qTotCap',
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

    def create_price_history_array(self, closing_price_objects):
        stock_price_history = []

        for element in closing_price_objects:
            priceChange = element.priceChange
            pricemin = element.priceMin
            pricemax = element.priceMax
            priceYesterday = element.priceYesterday
            priceFirst = element.priceFirst
            priceClosing = element.pClosing
            price_last_price_update_time = element.datetime_str

            stock_price_history.append((priceChange, pricemin, pricemax, priceYesterday, priceFirst, priceClosing
                                        , price_last_price_update_time))

        stock_price_history.sort(key=lambda x: datetime.strptime(x[-1], "%Y-%m-%d_%H-%M-%S"))

        return stock_price_history
