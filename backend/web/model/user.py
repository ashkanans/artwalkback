from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, DateTime, Sequence, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@dataclass
class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, Sequence('seq_users'), primary_key=True)
    username = Column(String(50))
    email = Column(String(50))
    password_hash = Column(String(50))
    created_at = Column(DateTime)
    notificationIsSet = Column(Boolean)
    last_update = Column(DateTime)
    params = Column(String(10))
    name = Column(String(50))
    sirname = Column(String(50))
