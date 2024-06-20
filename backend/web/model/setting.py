from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import declarative_base, registry

Base = declarative_base()
mapper_registry = registry()


class Setting(Base):
    __tablename__ = 'setting'
    __table_args__ = {'schema': 'web'}

    user_id = Column(Integer, nullable=False, primary_key=True)
    device_type = Column(String(50), nullable=False, primary_key=True)
    setting_key = Column(String(1000), nullable=False, primary_key=True)
    setting_value = Column(String(4000), nullable=False, primary_key=True)

    @classmethod
    def to_dict_list(cls, settings):
        return [
            {
                "setting_key": setting.setting_key,
                "setting_value": setting.setting_value
            } for setting in settings
        ]
