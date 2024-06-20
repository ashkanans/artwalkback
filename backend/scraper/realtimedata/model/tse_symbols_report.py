from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TseSymbolsReport(Base):
    __tablename__ = 'tse_symbols_report'

    # 78 columns of type Unicode(4000)

    A = Column(Unicode(4000), primary_key=True)
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


    def __init__(self, data):
        for i, value in enumerate(data):
            if i < 26:
                column_name = chr(65 + (i))
            else:
                first_letter = chr(65 + ((i) // 26 - 1))
                second_letter = chr(65 + ((i) % 26))
                column_name = f"{first_letter}{second_letter}"
            setattr(self, column_name, value)
