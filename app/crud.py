import logging
from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Link

logger = logging.getLogger(__name__)


async def create_link(db: AsyncSession, original_url: str, short_id: str) -> Link | None:
    """
    Создаёт новую короткую ссылку
    
    TODO: добавить проверку на дубликаты original_url!!!!! 
    TODO: добавить retry при коллизии short_id
    """
    
    if not original_url or not short_id:
        logger.warning(f"Ссылка с пустыми данными: url={original_url}, id={short_id}")
        raise ValueError("original_url и short_id не могут быть пустыми")
    
    link = Link(original_url=original_url, short_id=short_id)
    db.add(link)
    
    try:
        await db.commit()
        await db.refresh(link)
        return link
    except IntegrityError as e:
        
        await db.rollback()
        logger.error(f"Ошибка целостности при создании ссылки: {e}")
        
       
        return None
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Ошибка БД при создании ссылки: {e}")
        raise


async def get_link_by_short_id(db: AsyncSession, short_id: str) -> Link | None:
    """Находит ссылку по short_id. Возвращает None если не найдена."""
    try:
        result = await db.execute(
            select(Link).where(Link.short_id == short_id)
        )
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при поиске ссылки {short_id}: {e}")
        return None


async def increment_clicks(db: AsyncSession, short_id: str) -> bool:
    """
    Увеличивает счётчик
    
    """
    try:
       
        result = await db.execute(
            update(Link)
            .where(Link.short_id == short_id)
            .values(clicks=Link.clicks + 1)
            .returning(Link.id)  # проверка
        )
        await db.commit()
        
        updated = result.scalar_one_or_none() is not None
        if not updated:
            logger.warning(f"Попытка увеличить счётчик у несуществующей ссылки: {short_id}")
        return updated
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Ошибка при увеличении счётчика для {short_id}: {e}")
        return False


async def get_stats(db: AsyncSession, short_id: str) -> int | None:
    """
    Возвращает количество переходов по ссылке
    
    """
    try:
        result = await db.execute(
            select(Link.clicks).where(Link.short_id == short_id)
        )
        return result.scalar_one_or_none() 
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении статистики для {short_id}: {e}")
        return None


async def get_or_create_link(db: AsyncSession, original_url: str, short_id: str) -> Link:
    """
    Возвращает существующую ссылку или создаёт новую
    TODO: реализовать кэширование для частых запросов
    """

    existing = await get_link_by_short_id(db, short_id)
    if existing:
        return existing
    
    link = await create_link(db, original_url, short_id)
    if link is None:

        existing = await get_link_by_short_id(db, short_id)
        if existing:
            return existing
        raise RuntimeError(f"Не удалось создать ссылку {short_id}")
    
    return link
