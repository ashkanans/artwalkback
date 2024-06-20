from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper, ColumnProperty

Base = declarative_base()


class InstrumentInfo(Base):
    __tablename__ = 'tse_instrument_info'

    # Primary Key
    insCode = Column(Unicode(50), primary_key=True)

    # EPS Information
    epsValue = Column(Unicode(50))
    estimatedEPS = Column(Unicode(50))
    sectorPE = Column(Unicode(50))
    psr = Column(Unicode(50))

    # Sector Information
    cSecVal = Column(Unicode(50))
    lSecVal = Column(Unicode(50))

    # Static Threshold Information
    psGelStaMax = Column(Unicode(50))
    psGelStaMin = Column(Unicode(50))

    # Trading Range Information
    minWeek = Column(Unicode(50))
    maxWeek = Column(Unicode(50))
    minYear = Column(Unicode(50))
    maxYear = Column(Unicode(50))
    qTotTran5JAvg = Column(Unicode(50))
    kAjCapValCpsIdx = Column(Unicode(50))

    # General Information
    dEven = Column(Unicode(50))
    topInst = Column(Unicode(50))
    faraDesc = Column(Unicode(4000))
    contractSize = Column(Unicode(50))
    nav = Column(Unicode(50))
    underSupervision = Column(Unicode(50))
    cValMne = Column(Unicode(50))
    lVal18 = Column(Unicode(50))
    cSocCSAC = Column(Unicode(50))
    lSoc30 = Column(Unicode(50))
    yMarNSC = Column(Unicode(50))
    yVal = Column(Unicode(50))
    lVal30 = Column(Unicode(50))
    lVal18AFC = Column(Unicode(50))
    flow = Column(Unicode(50))
    cIsin = Column(Unicode(50))
    zTitad = Column(Unicode(50))
    baseVol = Column(Unicode(50))
    instrumentID = Column(Unicode(50))
    cgrValCot = Column(Unicode(50))
    cComVal = Column(Unicode(50))
    lastDate = Column(Unicode(50))
    sourceID = Column(Unicode(50))
    flowTitle = Column(Unicode(50))
    cgrValCotTitle = Column(Unicode(50))

    columns = [
        'insCode',
        'epsValue',
        'estimatedEPS',
        'sectorPE',
        'psr',
        'cSecVal',
        'lSecVal',
        'psGelStaMax',
        'psGelStaMin',
        'minWeek',
        'maxWeek',
        'minYear',
        'maxYear',
        'qTotTran5JAvg',
        'kAjCapValCpsIdx',
        'dEven',
        'topInst',
        'faraDesc',
        'contractSize',
        'nav',
        'underSupervision',
        'cValMne',
        'lVal18',
        'cSocCSAC',
        'lSoc30',
        'yMarNSC',
        'yVal',
        'lVal30',
        'lVal18AFC',
        'flow',
        'cIsin',
        'zTitad',
        'baseVol',
        'instrumentID',
        'cgrValCot',
        'cComVal',
        'lastDate',
        'sourceID',
        'flowTitle',
        'cgrValCotTitle',
    ]

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