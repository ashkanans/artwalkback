from sqlalchemy import Column, Unicode, Double
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ProfilesAtAGlance(Base):
    __tablename__ = 'profiles_at_a_glance'
    __table_args__ = {'schema': 'tgju'}

    Symbol = Column(Unicode(50), primary_key=True)

    CurrentRate = Column(Double)
    HighestDailyPrice = Column(Double)
    LowestDailyPrice = Column(Double)
    MaxDailyFluctuation = Column(Double)
    MaxFluctuationPercentage = Column(Unicode(50))
    MarketOpeningRate = Column(Double)
    LastRateRegistrationTime = Column(Unicode(50))
    PreviousDayRate = Column(Double)
    ChangePercentage = Column(Unicode(50))
    ChangeAmount = Column(Double)

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
        self.CurrentRate = data[1]
        self.HighestDailyPrice = data[2]
        self.LowestDailyPrice = data[3]
        self.MaxDailyFluctuation = data[4]
        self.MaxFluctuationPercentage = data[5]
        self.MarketOpeningRate = data[6]
        self.LastRateRegistrationTime = data[7]
        self.PreviousDayRate = data[8]
        self.ChangePercentage = data[9]
        self.ChangeAmount = data[10]
