import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from .config import settings

logger = logging.getLogger(__name__)

# Пока просто True для разраб, потом обязательно вынесу в конфиг
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False, 
)

Base = declarative_base()


async def get_db():
    """Зависимость для получения сессии БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger.exception("Database error")  # так ошибка с traceback
            await session.rollback()
            raise

