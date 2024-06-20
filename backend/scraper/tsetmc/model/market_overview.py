from sqlalchemy import Column, Unicode, Integer, Double
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MarketOverview(Base):
    __tablename__ = 'tse_market_overview'

    name = Column(Unicode(50), primary_key=True)
    lastDataDEven = Column(Integer)
    lastDataHEven = Column(Integer)
    indexLastValue = Column(Double)
    indexChange = Column(Double)
    indexEqualWeightedLastValue = Column(Double)
    indexEqualWeightedChange = Column(Double)
    marketActivityDEven = Column(Integer)
    marketActivityHEven = Column(Integer)
    marketActivityZTotTran = Column(Double)
    marketActivityQTotCap = Column(Double)
    marketActivityQTotTran = Column(Double)
    marketState = Column(Unicode(10))
    marketValue = Column(Unicode(50))
    marketValueBase = Column(Double)
    marketStateTitle = Column(Unicode(50))

    columns = [
        'name',
        'lastDataDEven',
        'lastDataHEven',
        'indexLastValue',
        'indexChange',
        'indexEqualWeightedLastValue',
        'indexEqualWeightedChange',
        'marketActivityDEven',
        'marketActivityHEven',
        'marketActivityZTotTran',
        'marketActivityQTotCap',
        'marketActivityQTotTran',
        'marketState',
        'marketValue',
        'marketValueBase',
        'marketStateTitle',
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
