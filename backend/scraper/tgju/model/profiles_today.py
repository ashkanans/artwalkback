from sqlalchemy import Column, Unicode, Double, Time, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ProfilesToday(Base):
    __tablename__ = 'profiles_today'
    __table_args__ = {'schema': 'tgju'}

    Key = Column(Unicode(100), primary_key=True)
    Symbol = Column(Unicode(50))
    Date = Column(Date)
    Price = Column(Double)
    Time = Column(Time)
    Change_Amount = Column(Unicode(50))
    Percentage_Change = Column(Unicode(50))

    def __init__(self, data):
        """
        Custom constructor to handle data conversion for ProfilesToday model.

        Parameters:
        - data (list): List containing profile today data.

        Example usage:
        profile_today_data = [
            'dollar_1402/2/2_02:09:33',
            'dollar',
            '1402/2/2',
            '940',
            '02:09:33',
            '-',
            '-'
        ]
        profile_today = ProfilesToday(profile_today_data)
        """
        super().__init__()

        self.Key = f"{data[0]} {data[1]} {data[3]}"
        self.Symbol = data[0]
        self.Date = data[1]
        self.Price = data[2]
        self.Time = data[3]
        self.Change_Amount = data[4]
        self.Percentage_Change = data[5]
