from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TseMarketView(Base):
    __tablename__ = 'tse_market_view'

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

    def __init__(self, data):
        for i, value in enumerate(data):
            if i <= 26:
                column_name = chr(65 + (i))
            else:
                first_letter = chr(65 + ((i) // 26 - 1))
                second_letter = chr(65 + ((i) % 26))
                column_name = f"{first_letter}{second_letter}"
            setattr(self, column_name, value)
