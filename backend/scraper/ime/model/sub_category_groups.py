from sqlalchemy import Column, Unicode
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SubCategoryGroups(Base):
    __tablename__ = "ime_sub_category_groups"

    code = Column(Unicode(50), primary_key=True)
    name = Column(Unicode(50))
