from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from .personality import Personality
from .bot_info import BotInfo

DB_PATH = "bots.db"
Base = declarative_base()


class BotDB:
    def __init__(self, db_path=DB_PATH):
        self.engine = create_async_engine(db_path, echo=True)
        self.Session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_personality(self, creator_id: int, name: str, description: str):
        async with self.Session() as session:
            new_personality = Personality(creator_id=creator_id, name=name, description=description)
            session.add(new_personality)
            try:
                await session.commit()
            except SQLAlchemyError:
                await session.rollback()

    async def get_personalities(self, user_id: int):
        async with self.Session() as session:
            result = await session.execute(select(Personality).where(Personality.creator_id == user_id))
            return result.scalars().all()

    async def update_personality(self, personality_id: int, name: str, description: str):
        async with self.Session() as session:
            try:
                personality = await session.get(Personality, personality_id)
                if personality:
                    personality.name = name
                    personality.description = description
                    await session.commit()
            except SQLAlchemyError:
                await session.rollback()

    async def delete_personality(self, personality_id: int):
        async with self.Session() as session:
            try:
                personality = await session.get(Personality, personality_id)
                if personality:
                    await session.delete(personality)
                    await session.commit()
            except SQLAlchemyError:
                await session.rollback()

    async def add_bot_info(self, bot_id: int, scenario: str, initial_message: str):
        async with self.Session() as session:
            new_bot_info = BotInfo(id=bot_id, scenario=scenario, initial_message=initial_message)
            session.add(new_bot_info)
            try:
                await session.commit()
            except SQLAlchemyError:
                await session.rollback()

    async def get_bot_info(self, bot_id: int):
        async with self.Session() as session:
            result = await session.execute(select(BotInfo).where(BotInfo.id == bot_id))
            return result.scalars().first()

    async def update_bot_scenario(self, bot_id: int, scenario: str):
        async with self.Session() as session:
            try:
                bot_info = await session.get(BotInfo, bot_id)
                if bot_info:
                    bot_info.scenario = scenario
                    await session.commit()
            except SQLAlchemyError:
                await session.rollback()

    async def update_bot_initial_message(self, bot_id: int, initial_message: str):
        async with self.Session() as session:
            try:
                bot_info = await session.get(BotInfo, bot_id)
                if bot_info:
                    bot_info.initial_message = initial_message
                    await session.commit()
            except SQLAlchemyError:
                await session.rollback()

    async def delete_bot_info(self, bot_id: int):
        async with self.Session() as session:
            try:
                bot_info = await session.get(BotInfo, bot_id)
                if bot_info:
                    await session.delete(bot_info)
                    await session.commit()
            except SQLAlchemyError:
                await session.rollback()

    async def get_description(self, user_id: int, name: str):
        async with self.Session() as session:
            result = await session.execute(
                select(Personality.description).where(Personality.creator_id == user_id, Personality.name == name)
            )
            return result.scalar()

    async def get_bot_scenario(self, bot_id: int):
        async with self.Session() as session:
            result = await session.execute(select(BotInfo.scenario).where(BotInfo.id == bot_id))
            return result.scalar()

    async def get_bot_initial_message(self, bot_id: int):
        async with self.Session() as session:
            result = await session.execute(select(BotInfo.initial_message).where(BotInfo.id == bot_id))
            return result.scalar()

