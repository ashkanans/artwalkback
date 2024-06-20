from sqlalchemy import Column, Unicode, Double
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ProfilesPerformance(Base):
    __tablename__ = 'profiles_performance'
    __table_args__ = {'schema': 'tgju'}

    Name = Column(Unicode(50))
    Symbol = Column(Unicode(50), primary_key=True)
    One_Day = Column(Double)
    One_Week = Column(Double)
    One_Month = Column(Double)
    Six_Month = Column(Double)
    One_Year = Column(Double)
    Three_Years = Column(Double)

    def __init__(self, data):
        """
        Custom constructor to handle data conversion for ProfilesPerformance model.

        Parameters:
        - data (dict): Dictionary containing performance profile data.

        Example usage:
        performance_data = {
            'Symbol': 'ABC',
            'One_Week': '10%',
            'One_Month': '15%',
            'One_Day': '5%',
            'Name': 'Company ABC',
            'Three_Years': '50%',
            'One_Year': '30%',
            'Six_Month': '25%'
        }
        performance_profile = ProfilesPerformance(**performance_data)
        """
        super().__init__()

        self.Symbol = data[0]
        self.Name = data[1]
        self.One_Day = data[2]
        self.One_Week = data[3]
        self.One_Month = data[4]
        self.Six_Month = data[5]
        self.Three_Years = data[6]
        self.One_Year = data[7]

