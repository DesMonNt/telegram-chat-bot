from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import declarative_base


class Personality(declarative_base()):
    __tablename__ = 'personalities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    __table_args__ = (UniqueConstraint('user_id', 'name'),)