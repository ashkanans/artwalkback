from sqlalchemy import Column, Integer, NVARCHAR, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Letter(Base):
    __tablename__ = 'Letter'
    __table_args__ = {'schema': 'CODAL'}

    TracingNo = Column(Integer, primary_key=True)
    Symbol = Column(NVARCHAR(4000), primary_key=True)
    Title = Column(NVARCHAR(4000), primary_key=True)
    PublishDateTime = Column(NVARCHAR(4000), primary_key=True)
    CompanyName = Column(NVARCHAR(4000), primary_key=True)
    Url = Column(NVARCHAR(4000), primary_key=True)
    AttachmentUrl = Column(NVARCHAR(4000), primary_key=True)
    keyword = Column(NVARCHAR(50), primary_key=True)
    isSeen = Column(Boolean, primary_key=True)

    def __init__(self, TracingNo, Symbol, Title, PublishDateTime, CompanyName, Url, AttachmentUrl, keyword, isSeen):
        self.TracingNo = TracingNo
        self.Symbol = Symbol
        self.Title = Title
        self.PublishDateTime = PublishDateTime
        self.CompanyName = CompanyName
        self.Url = Url
        self.AttachmentUrl = AttachmentUrl
        self.keyword = keyword
        self.isSeen = isSeen

    def to_dict(self):
        return {
            'TracingNo': self.TracingNo,
            'Symbol': self.Symbol,
            'Title': self.Title,
            'PublishDateTime': self.PublishDateTime,
            'persian_company_name': self.CompanyName,
            'Url': self.Url,
            'AttachmentUrl': self.AttachmentUrl,
            'Isseen': self.isSeen,
            'containingWords': {self.keyword: '1'}
        }