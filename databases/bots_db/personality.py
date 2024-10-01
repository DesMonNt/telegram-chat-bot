from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


class Personality(declarative_base()):
    __tablename__ = 'personalities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    creator_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)