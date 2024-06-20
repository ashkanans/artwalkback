from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Tables(Base):
    __tablename__ = 'codal_letters_map_sheets_tables'

    # Columns
    tablesId = Column(Unicode(50), primary_key=True)
    metaTableId = Column(Unicode(50))
    title_En = Column(Unicode(500))
    title_Fa = Column(Unicode(500))
    sequence = Column(Unicode(50))
    sheetCode = Column(Unicode(50))
    code = Column(Unicode(50))
    description = Column(Unicode(50))
    aliasName = Column(Unicode(50))
    versionNo = Column(Unicode(50))
    cellsId = Column(Unicode(50))
