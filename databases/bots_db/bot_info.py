from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey


class BotInfo(declarative_base()):
    __tablename__ = 'bot_info'
    id = Column(Integer, ForeignKey('personalities.id'), primary_key=True, autoincrement=True)
    scenario = Column(String)
    initial_message = Column(String)