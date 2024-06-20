from sqlalchemy import Unicode, Column, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import ColumnProperty, class_mapper

Base = declarative_base()


class Letter(Base):
    __tablename__ = 'codal_letters'

    LetterId = Column(Unicode(50), Sequence('seq_codal_letters_MAR1MP'), primary_key=True)
    InsCode = Column(Unicode(50))
    TracingNo = Column(Unicode(50))
    Symbol = Column(Unicode(50))
    CompanyName = Column(Unicode(500))
    UnderSupervision = Column(Unicode(50))
    Title = Column(Unicode(500))
    LetterCode = Column(Unicode(50))
    SentDateTime = Column(Unicode(50))
    PublishDateTime = Column(Unicode(50))
    HasHtml = Column(Unicode(50))
    IsEstimate = Column(Unicode(50))
    Url = Column(Unicode(500))
    HasExcel = Column(Unicode(50))
    HasPdf = Column(Unicode(50))
    HasXbrl = Column(Unicode(50))
    HasAttachment = Column(Unicode(50))
    AttachmentUrl = Column(Unicode(500))
    PdfUrl = Column(Unicode(500))
    ExcelUrl = Column(Unicode(500))
    XbrlUrl = Column(Unicode(500))
    TedanUrl = Column(Unicode(500))
    FinancialYearUntil = Column(Unicode(50))

    @classmethod
    def list_of_objects_to_dict_list(cls, object_list):
        """
        Convert a list of Letter objects to a list of dictionaries.

        Args:
        - object_list (list): List of Letter objects.

        Returns:
        - list: List of dictionaries where keys are column names and values are object fields.
        """
        if not object_list:
            return []

        # Get column names from the class mapper
        column_names = [prop.key for prop in class_mapper(cls).iterate_properties
                        if isinstance(prop, ColumnProperty)]

        # Create a list of dictionaries
        dict_list = [dict((col, getattr(obj, col)) for col in column_names) for obj in object_list]

        return dict_list
