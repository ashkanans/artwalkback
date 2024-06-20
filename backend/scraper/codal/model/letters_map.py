from sqlalchemy import Column, NVARCHAR, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class LetterMAP(Base):
    __tablename__ = 'codal_letters_map'

    # Existing columns
    annID = Column(NVARCHAR(50), Sequence('Seq_codal_letters_map'), primary_key=True)
    listedCapital = Column(NVARCHAR(50))
    unauthorizedCapital = Column(NVARCHAR(50))
    reportName = Column(NVARCHAR(50))
    companyState = Column(NVARCHAR(50))
    company = Column(NVARCHAR(50))
    symbol = Column(NVARCHAR(50))
    isic = Column(NVARCHAR(50))

    # New columns from the dictionary
    title_Fa = Column(NVARCHAR(255))  # Assuming the title can be longer
    title_En = Column(NVARCHAR(255))
    subject = Column(NVARCHAR(255))
    dsc = Column(NVARCHAR(255))
    type = Column(NVARCHAR(50))
    period = Column(NVARCHAR(50))
    periodEndToDate = Column(NVARCHAR(10))  # Adjust the length as needed
    yearEndToDate = Column(NVARCHAR(10))  # Adjust the length as needed
    periodExtraDay = Column(NVARCHAR(50))
    isConsolidated = Column(NVARCHAR(50))
    tracingNo = Column(NVARCHAR(50))
    kind = Column(NVARCHAR(50))
    isAudited = Column(NVARCHAR(50))
    auditState = Column(NVARCHAR(50))
    registerDateTime = Column(NVARCHAR(19))  # Assuming datetime format
    sentDateTime = Column(NVARCHAR(19))  # Assuming datetime format
    publishDateTime = Column(NVARCHAR(19))  # Assuming datetime format
    state = Column(NVARCHAR(50))
    isForAuditing = Column(NVARCHAR(50))
    sheetsId = Column(NVARCHAR(50))
