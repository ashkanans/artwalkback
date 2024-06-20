from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database_config.config import SQL_SERVER_URL
from backend.web.model.setting import Setting

# Creating the SQLAlchemy engine
engine = create_engine(SQL_SERVER_URL)
Session = sessionmaker(bind=engine)
session = Session()


class SettingService:
    def __init__(self):
        pass

    def set_setting_by_user(self, user_id, setting_values, device_type):

        for setting_key, setting_value in setting_values.items():
            setting = session.query(Setting).filter_by(
                user_id=user_id,
                device_type=device_type,
                setting_key=setting_key
            ).first()

            if setting:
                setting.setting_value = setting_value
            else:
                setting = Setting(
                    user_id=user_id,
                    device_type=device_type,
                    setting_key=setting_key,
                    setting_value=setting_value
                )
                session.add(setting)

        session.commit()

    def get_setting_by_user_id_device_type(self, user_id, device_type):

        settings = session.query(Setting).filter_by(user_id=user_id, device_type=device_type).all()

        session.commit()

        return settings

    def delete_rows_by_user_id(self, user_id):
        try:
            settings_to_delete = session.query(Setting).filter_by(user_id=user_id).all()

            for setting in settings_to_delete:
                session.delete(setting)

            session.commit()

        except Exception as e:
            session.rollback()
            raise e

