from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserNotification(Base):
    __tablename__ = 'Users_Notification'
    __table_args__ = {'schema': 'web'}

    user_id = Column(String(50), primary_key=True)
    tracingNo = Column(String(50), primary_key=True)
    keyword = Column(String(50), primary_key=True)
    isSeen = Column(Boolean, primary_key=True)
