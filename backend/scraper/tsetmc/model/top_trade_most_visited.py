from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper, ColumnProperty

Base = declarative_base()


class TradeTopMostVisited(Base):
    __tablename__ = 'tse_trade_top_most_visited'

    marketName = Column(Unicode(50))
    instrumentState = Column(Unicode(50))
    lastHEven = Column(Unicode(50))
    finalLastDate = Column(Unicode(50))
    nvt = Column(Unicode(50))
    mop = Column(Unicode(50))
    pRedTran = Column(Unicode(50))
    thirtyDayClosingHistory = Column(Unicode(50))
    priceChange = Column(Unicode(50))
    priceMin = Column(Unicode(50))
    priceMax = Column(Unicode(50))
    priceYesterday = Column(Unicode(50))
    priceFirst = Column(Unicode(50))
    last = Column(Unicode(50))
    id = Column(Unicode(50))
    insCode = Column(Unicode(50), primary_key=True)
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
        'marketName',
        'instrumentState',
        'lastHEven',
        'finalLastDate',
        'nvt',
        'mop',
        'pRedTran',
        'thirtyDayClosingHistory',
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
        Convert a list of MarketOverview objects to a list of dictionaries.

        Args:
        - object_list (list): List of MarketOverview objects.

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
