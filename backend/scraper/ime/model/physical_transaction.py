from sqlalchemy import Column, Unicode, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PhysicalTransaction(Base):
    __tablename__ = 'ime_physical_transaction'

    id = Column(Unicode(50), Sequence('seq_physical_transcation_id'), primary_key=True)
    Symbol = Column(Unicode(500))
    GoodsName = Column(Unicode(500))
    ProducerName = Column(Unicode(500))
    ContractType = Column(Unicode(500))
    MinPrice = Column(Unicode(50))
    Price = Column(Unicode(50))
    MaxPrice = Column(Unicode(50))
    arze = Column(Unicode(50))
    ArzeBasePrice = Column(Unicode(50))
    arzeMinPrice = Column(Unicode(50))
    taghaza = Column(Unicode(50))
    taghazavoroudi = Column(Unicode(50))
    taghazaMaxPrice = Column(Unicode(50))
    Quantity = Column(Unicode(50))
    TotalPrice = Column(Unicode(50))
    date = Column(Unicode(50))
    DeliveryDate = Column(Unicode(50))
    Warehouse = Column(Unicode(50))
    ArzehKonandeh = Column(Unicode(500))
    SettlementDate = Column(Unicode(50))
    Category = Column(Unicode(50))
    xTalarReportPK = Column(Unicode(50))
    bArzehRadifTarSarresid = Column(Unicode(50))
    cBrokerSpcName = Column(Unicode(50))
    ModeDescription = Column(Unicode(50))
    MethodDescription = Column(Unicode(50))
    MinPrice1 = Column(Unicode(50))
    Price1 = Column(Unicode(50))
    Currency = Column(Unicode(50))
    Unit = Column(Unicode(50))
    arzehPk = Column(Unicode(50))
    Talar = Column(Unicode(50))
    PacketName = Column(Unicode(50))
    Tasvieh = Column(Unicode(50))
