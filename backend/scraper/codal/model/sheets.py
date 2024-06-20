from sqlalchemy import Column, Unicode

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Sheets(Base):
    __tablename__ = 'codal_letters_map_sheets'

    sheetsId = Column(Unicode(50))
    code = Column(Unicode(50))
    title_Fa = Column(Unicode(500))
    title_En = Column(Unicode(500))
    sequence = Column(Unicode(50))
    isDynamic = Column(Unicode(50))
    tablesId = Column(Unicode(50), primary_key=True)
    aliasName = Column(Unicode(500))
    versionNo = Column(Unicode(50))
    sheetComponentsId = Column(Unicode(50))
