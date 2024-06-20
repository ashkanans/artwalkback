from sqlalchemy import Unicode, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import ColumnProperty, class_mapper

Base = declarative_base()


class Categories(Base):
    __tablename__ = 'tradingeconomics_categories'

    name = Column(Unicode(50), primary_key=True)
    link = Column(Unicode(50))

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
