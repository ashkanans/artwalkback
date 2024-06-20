from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PreparedData(Base):
    __tablename__ = 'tse_prepared_data'

    id = Column(Unicode(50), primary_key=True)
    symbol = Column(Unicode(50))
    name = Column(Unicode(500))
    title = Column(Unicode(4000))
    sentDateTime_Gregorian = Column(Unicode(50))
    publishDateTime_Gregorian = Column(Unicode(50))
    publishDateTime_DEven = Column(Unicode(50))
    mainTableRowID = Column(Unicode(50))
    hasHtmlReport = Column(Unicode(50))
    hasExcelReport = Column(Unicode(50))
    hasPDFReport = Column(Unicode(50))
    hasXMLReport = Column(Unicode(50))
    attachmentID = Column(Unicode(50))
    contentType = Column(Unicode(50))
    fileName = Column(Unicode(50))
    fileExtension = Column(Unicode(50))
    tracingNo = Column(Unicode(50))
