from sqlalchemy import Column, Unicode, Sequence, Index, UnicodeText
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Cells(Base):
    __tablename__ = 'codal_letters_map_sheets_tables_cells'

    prKey = Column(Unicode(50), Sequence('Seq_codal_letters_map_sheets_tables_cells'), primary_key=True)
    cellId = Column(Unicode(50))
    financialConcept = Column(Unicode(500))
    cellGroupName = Column(Unicode(50))
    validations = Column(Unicode(500))
    formula = Column(Unicode(500))
    address = Column(Unicode(50))
    rowSpan = Column(Unicode(50))
    rowCode = Column(Unicode(50))
    metaTableCode = Column(Unicode(50))
    metaTableId = Column(Unicode(50))
    rowSequence = Column(Unicode(50))
    colSpan = Column(Unicode(50))
    columnCode = Column(Unicode(50))
    columnSequence = Column(Unicode(50))
    cssClass = Column(Unicode(500))
    rowTypeName = Column(Unicode(500))
    category = Column(Unicode(50))
    isVisible = Column(Unicode(50))
    value = Column(UnicodeText)
    valueTypeName = Column(Unicode(500))
    dataTypeName = Column(Unicode(500))
    decimalPlace = Column(Unicode(50))
    periodEndToDate = Column(Unicode(50))
    yearEndToDate = Column(Unicode(50))
    conditionalIsUnique = Column(Unicode(50))
    removableCustomRow = Column(Unicode(50))


# Define indexes for the 'Cells' table
Index('idx_cellId', Cells.cellId)
