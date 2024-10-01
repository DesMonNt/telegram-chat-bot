from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base


class UserSettings(declarative_base()):
    __tablename__ = 'user_settings'
    user_id = Column(Integer, primary_key=True)
    active_personality = Column(String, ForeignKey('personalities.name'))