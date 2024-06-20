import datetime

import jdatetime
from sqlalchemy import Column, Unicode, MetaData, Date, Double
from sqlalchemy.orm import declarative_base

from backend.utils.scraper.tgju.utils import extract_number_from_span

Base = declarative_base()

metadata = MetaData(schema='tgju')


class ProfilesSummary(Base):
    __tablename__ = 'profiles_summary'
    __table_args__ = ({'schema': 'tgju'},

                      )

    PrKey = Column(Unicode(50), primary_key=True)
    Symbol = Column(Unicode(50))
    Opening = Column(Double(50))
    Minimum = Column(Double(50))
    Maximum = Column(Double(50))
    Closing = Column(Double(50))
    Change_Amount = Column(Unicode(50))
    Percentage_Change = Column(Unicode(50))
    Date_Gregorian = Column(Date)
    Date_Solar = Column(Unicode(50))

    def __init__(self, data):
        """
        Custom constructor to handle data conversion for TgjuProfiles model.

        Parameters:
        - data (dict): Dictionary containing tgju profile data.

        Example usage:
        tgju_profile_data = {
            0: "26,266",
            1: "26,266",
            2: "26,283",
            3: "26,275",
            4: '<span class="high" dir="ltr">69</span>',
            5: '<span class="high" dir="ltr">0.26%</span>',
            6: "2024/01/10",
            7: "1402/10/20"
        }
        tgju_profile = TgjuProfiles(**tgju_profile_data)
        """
        super().__init__()

        self.Symbol = data[0]

        self.Opening = data[1]
        self.Minimum = data[2]
        self.Maximum = data[3]
        self.Closing = data[4]
        self.Change_Amount = extract_number_from_span(data[5])
        self.Percentage_Change = extract_number_from_span(data[6])
        self.Date_Gregorian = datetime.datetime.strptime(data[7], '%Y/%m/%d').date()
        self.Date_Solar = str(jdatetime.date.fromgregorian(day=self.Date_Gregorian.day, month=self.Date_Gregorian.month,
                                                           year=self.Date_Gregorian.year))
        self.PrKey = f"{self.Symbol} - {self.Date_Gregorian}"
