from collections import defaultdict

from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def ids_list_to_dict_list(objects_list):
    result_final = defaultdict(list)
    result = defaultdict(list)

    for item in objects_list:
        type = ""
        if item.type == "دلاري":
            type = "dollar"
        elif item.type == "نسبي":
            type = "nesbi"
        elif item.type == "ريالي":
            type = "rial"
        result[type].append(item)

    for type_, items in result.items():
        type_dict = defaultdict(list)
        for item in items:
            type_dict[item.category_id].append(
                {"ID": item.ID, "Name_fa": item.Name_fa, "category_fa": item.category_fa})
        result_final[type_] = [{"category_id": k, "category_fa": v[0].get('category_fa'), "data": v} for k, v in
                               type_dict.items()]

    return result_final


class BusinessInsiderID(Base):
    __tablename__ = 'ID'
    category_id = Column(String(255), primary_key=True, nullable=True)
    category_fa = Column(String(255), primary_key=True, nullable=True)
    type = Column(String(255), primary_key=True, nullable=True)
    ID = Column(String(255), primary_key=True)
    Name_fa = Column(String(255), primary_key=True, nullable=True)
