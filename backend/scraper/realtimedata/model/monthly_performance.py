from sqlalchemy import Column, Unicode, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MonthlyPerformance(Base):
    __tablename__ = 'monthly_performance'

    # 78 columns of type Unicode(4000)
    Id = Column(Integer, primary_key=True)
    A = Column(Unicode(4000))
    B = Column(Unicode(4000))
    C = Column(Unicode(4000))
    D = Column(Unicode(4000))
    E = Column(Unicode(4000))
    F = Column(Unicode(4000))
    G = Column(Unicode(4000))
    H = Column(Unicode(4000))
    I = Column(Unicode(4000))
    J = Column(Unicode(4000))
    K = Column(Unicode(4000))
    L = Column(Unicode(4000))
    M = Column(Unicode(4000))
    N = Column(Unicode(4000))
    O = Column(Unicode(4000))
    P = Column(Unicode(4000))
    Q = Column(Unicode(4000))
    R = Column(Unicode(4000))
    S = Column(Unicode(4000))
    T = Column(Unicode(4000))
    U = Column(Unicode(4000))
    V = Column(Unicode(4000))
    W = Column(Unicode(4000))
    X = Column(Unicode(4000))
    Y = Column(Unicode(4000))
    Z = Column(Unicode(4000))
    AA = Column(Unicode(4000))
    AB = Column(Unicode(4000))
    AC = Column(Unicode(4000))
    AD = Column(Unicode(4000))
    AE = Column(Unicode(4000))
    AF = Column(Unicode(4000))
    AG = Column(Unicode(4000))
    AH = Column(Unicode(4000))
    AI = Column(Unicode(4000))
    AJ = Column(Unicode(4000))
    AK = Column(Unicode(4000))
    AL = Column(Unicode(4000))
    AM = Column(Unicode(4000))
    AN = Column(Unicode(4000))
    AO = Column(Unicode(4000))
    AP = Column(Unicode(4000))
    AQ = Column(Unicode(4000))
    AR = Column(Unicode(4000))
    AS = Column(Unicode(4000))
    AT = Column(Unicode(4000))
    AU = Column(Unicode(4000))
    AV = Column(Unicode(4000))
    AW = Column(Unicode(4000))
    AX = Column(Unicode(4000))
    AY = Column(Unicode(4000))
    AZ = Column(Unicode(4000))
    BA = Column(Unicode(4000))
    BB = Column(Unicode(4000))
    BC = Column(Unicode(4000))
    BD = Column(Unicode(4000))
    BE = Column(Unicode(4000))
    BF = Column(Unicode(4000))
    BG = Column(Unicode(4000))
    BH = Column(Unicode(4000))
    BI = Column(Unicode(4000))
    BJ = Column(Unicode(4000))
    BK = Column(Unicode(4000))
    BL = Column(Unicode(4000))
    BM = Column(Unicode(4000))
    BN = Column(Unicode(4000))
    BO = Column(Unicode(4000))
    BP = Column(Unicode(4000))
    BQ = Column(Unicode(4000))
    BR = Column(Unicode(4000))
    BS = Column(Unicode(4000))
    BT = Column(Unicode(4000))
    BU = Column(Unicode(4000))
    BV = Column(Unicode(4000))
    BW = Column(Unicode(4000))
    BX = Column(Unicode(4000))
    BY = Column(Unicode(4000))
    BZ = Column(Unicode(4000))

    def __init__(self, data):
        self.Id = data[0]
        for i, value in enumerate(data[1:], start=1):
            column_name = chr(65 + (i - 1) % 26)
            if i > 26:
                column_name = 'A' + column_name
            setattr(self, column_name, value)
