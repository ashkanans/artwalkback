from collections import defaultdict

from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper

Base = declarative_base()


class FirstPageTablesRows(Base):
    __tablename__ = 'first_page_tables_rows'

    nameFa = Column(String(255), primary_key=True)
    nameEn = Column(String(255), primary_key=True)
    tableId = Column(String(255), primary_key=True)
    p = Column(String(255), primary_key=True)
    h = Column(String(255), primary_key=True)
    l = Column(String(255), primary_key=True)
    d = Column(String(255), primary_key=True)
    dp = Column(String(255), primary_key=True)
    dt = Column(String(255), primary_key=True)
    t = Column(String(255), primary_key=True)
    t_g = Column(String(255), primary_key=True)
    ts = Column(String(255), primary_key=True)

    def to_dict(self):
        """
        Convert the object to a dictionary.
        """
        result = {}
        for column in class_mapper(self.__class__).columns:
            result[column.name] = getattr(self, column.name)
        return result

    @staticmethod
    def group_by_table_id(rows_list):
        """
        Group rows by tableId into a dictionary.

        Args:
            rows_list (list of FirstPageTablesRows): List of rows.

        Returns:
            dict: Dictionary with tableId as keys and a list of dicts of rows as values.
        """
        grouped_dict = defaultdict(list)
        for row in rows_list:
            row_dict = row.to_dict()
            table_id = row_dict['tableId']
            grouped_dict[table_id].append(row_dict)
        return grouped_dict
