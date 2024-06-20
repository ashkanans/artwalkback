from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def ids_list_to_dict_list(objects_list):
    result_dict = {}

    for obj in objects_list:
        if obj.level1 not in result_dict:
            result_dict[obj.level1] = {}
        if obj.level2 not in result_dict[obj.level1]:
            result_dict[obj.level1][obj.level2] = {}
        if obj.level3 not in result_dict[obj.level1][obj.level2]:
            result_dict[obj.level1][obj.level2][obj.level3] = []

        result_dict[obj.level1][obj.level2][obj.level3].append({
            'level4': obj.level4,
            'level4_id': obj.level4_id
        })

    return result_dict


class ChartIDs(Base):
    __tablename__ = 'chart_IDs'
    __table_args__ = {'schema': 'app'}

    level1 = Column(String, primary_key=True, nullable=True)
    level2 = Column(String, primary_key=True, nullable=True)
    level3 = Column(String, primary_key=True, nullable=True)
    level4 = Column(String, primary_key=True, nullable=True)
    level4_id = Column(String, primary_key=True, autoincrement=False)

    def __init__(self, level1=None, level2=None, level3=None, level4=None, level4_id=None):
        self.level1 = level1
        self.level2 = level2
        self.level3 = level3
        self.level4 = level4
        self.level4_id = level4_id
