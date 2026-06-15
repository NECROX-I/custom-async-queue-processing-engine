from collections.abc import AsyncGenerator

from loguru import logger

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from sqlalchemy.orm import DeclarativeBase

from core.config import settings

#one engine for the entire application
engine = create_async_engine (settings.database_url, echo=settings.is_development, pool_pre_ping=True, poolsize=10, max_overflow=20)

# session
AsyncSessionFactory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

#declarative base all models import from this base
class Base(DeclarativeBase):
    pass

#dependency for getting db session
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database error: {e}")
            raise

#shutdown db
async def init_db():
    async with engine.connect() as conn:
        await conn.execute(__import__("sqlalchemy").text("SELECT 1"))
    logger.info("Database connected -{}",settings.database_url.split('@')[-1])

async def shutdown_db()-> None:
    await engine.dispose()
    logger.info("Database connection closed")   