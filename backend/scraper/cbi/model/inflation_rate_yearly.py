from sqlalchemy import Column, Integer, Float, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper, ColumnProperty

Base = declarative_base()


class InflationRateYearly(Base):
    __tablename__ = 'cbi_inflation_rates_yearly'
    __table_args__ = (Index('idx_year_unique', 'Year', unique=True),)

    # Primary Key
    Id = Column(Integer, primary_key=True, autoincrement=True)
    # Id = Column(Integer, Sequence("Seq_Inflation_Rate"), primary_key=True)
    Year = Column(Integer)
    Index = Column(Float)
    InflationRate = Column(Float)

    @classmethod
    def list_of_objects_to_dict_list(cls, object_list):
        """
        Convert a list of InstrumentInfo objects to a list of dictionaries.

        Args:
        - object_list (list): List of InstrumentInfo objects.

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

    def flat_to_nested(self):
        nested_data = {
            'Instrument Info': {
                "Inst. ID": self.instrumentID,
                "Inst. Name En": self.lVal18,
                "Inst. Name Fa": self.lVal30,
                "Inst. Acronyms Fa": self.lVal18AFC,
                "Inst. Sec. ID": self.cSecVal,
                "Inst. Sec. Name": self.lSecVal
            },
            'Financial Ratios': {
                'EPS': self.epsValue,
                "P/E Ratio": self.estimatedEPS,
                "Group P/E Ratio": self.sectorPE,
                'P/S Ratio': self.psr
            },
            'Price Ranges': {
                "Price Range - Upper Limit": self.psGelStaMax,
                "Price Range - Lower Limit": self.psGelStaMin,
                "Weekly Price Range - High": self.maxWeek,
                "Weekly Price Range - Low": self.minWeek,
                "Yearly Price Range - High": self.maxYear,
                "Yearly Price Range - Low": self.minYear
            },
            'Trading Information': {
                "Number of Shares": self.zTitad,
                "Base Volume": self.baseVol,
                "Floating Shares Percentage": self.kAjCapValCpsIdx,
                "Monthly Average Volume": self.qTotTran5JAvg
            },
            'Transaction Prices': {
                # Add the relevant mappings for Transaction_Prices here
            },
            'Transaction Statistics': {
                # Add the relevant mappings for Transaction_Statistics here
            },
            'Volume Information': {
                # Add the relevant mappings for Volume_Information here
            },
            'Shares Information': {
                # Add the relevant mappings for Shares_Information here
            },
        }

        return nested_data
