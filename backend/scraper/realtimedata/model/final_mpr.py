from sqlalchemy import Column, Unicode, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FinalMpr(Base):
    __tablename__ = 'final_mpr'

    # 50 columns of type Unicode(4000)
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

    def __init__(self, data):
        self.Id = data[0]
        for i in range(1, min(len(data), 53)):
            setattr(self, chr(65 + i - 1), data[i])
