from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from .user_settings import UserSettings
from .personality import Personality

DATABASE_URL = "personalities.db"
Base = declarative_base()


class PersonalityDB:
    def __init__(self):
        self.engine = create_async_engine(DATABASE_URL, echo=True)
        self.async_session = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_personality(self, user_id: int, name: str, description: str):
        async with self.async_session() as session:
            try:
                new_personality = Personality(user_id=user_id, name=name, description=description)
                session.add(new_personality)
                await session.commit()
            except SQLAlchemyError:
                await session.rollback()

    async def get_personalities(self, user_id: int):
        async with self.async_session() as session:
            async with session.begin():
                result = await session.execute(select(Personality).where(Personality.user_id == user_id))
                return result.scalars().all()

    async def update_personality(self, user_id: int, name: str, new_description: str):
        async with self.async_session() as session:
            try:
                result = await session.execute(
                    select(Personality).where(Personality.user_id == user_id, Personality.name == name)
                )
                personality = result.scalars().first()
                if personality:
                    personality.description = new_description
                    await session.commit()
            except SQLAlchemyError:
                await session.rollback()

    async def delete_personality(self, user_id: int, name: str):
        async with self.async_session() as session:
            try:
                result = await session.execute(
                    select(Personality).where(Personality.user_id == user_id, Personality.name == name)
                )
                personality = result.scalars().first()
                if personality:
                    await session.delete(personality)
                    await session.commit()
            except SQLAlchemyError:
                await session.rollback()

    async def set_active_personality(self, user_id: int, name: str):
        async with self.async_session() as session:
            try:
                result = await session.execute(select(UserSettings).where(UserSettings.user_id == user_id))
                user_settings = result.scalars().first()

                if user_settings:
                    user_settings.active_personality = name
                else:
                    user_settings = UserSettings(user_id=user_id, active_personality=name)
                    session.add(user_settings)

                await session.commit()
            except SQLAlchemyError:
                await session.rollback()

    async def get_active_personality(self, user_id: int):
        async with self.async_session() as session:
            result = await session.execute(select(UserSettings.active_personality).where(UserSettings.user_id == user_id))
            active_personality = result.scalar()
            return active_personality

    async def get_description(self, user_id: int, name: str):
        async with self.async_session() as session:
            result = await session.execute(
                select(Personality.description).where(Personality.user_id == user_id, Personality.name == name)
            )
            description = result.scalar()
            return description
