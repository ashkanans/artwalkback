from sqlalchemy import Column, String, BINARY
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OCRConvertedFile(Base):
    __tablename__ = 'ocr_converted_files'

    id = Column(String(50), primary_key=True)
    type = Column(String(10), nullable=False)
    name = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    converted_word = Column(BINARY, nullable=False)
    converted_txt = Column(BINARY, nullable=False)
    source = Column(String(50), nullable=True)
    insert_date_time = Column(String(50), nullable=True)
