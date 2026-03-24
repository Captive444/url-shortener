from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud, schemas, utils
from ..config import settings
from ..database import get_db

router = APIRouter(tags=["links"])


@router.post("/shorten", response_model=schemas.LinkResponse)
async def shorten_link(
    link: schemas.LinkCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создаёт короткую ссылку из длинной"""
    
    
    short_id = utils.generate_short_id(settings.SHORT_ID_LENGTH)
    
    
    existing = await crud.get_link_by_short_id(db, short_id)
    while existing:
        short_id = utils.generate_short_id(settings.SHORT_ID_LENGTH)
        existing = await crud.get_link_by_short_id(db, short_id)
    
  
    db_link = await crud.create_link(
        db,
        original_url=str(link.url),
        short_id=short_id
    )
    
    # Формирует короткую ссылку
    short_url = f"{settings.BASE_URL}/{db_link.short_id}"
    
    return schemas.LinkResponse(short_id=db_link.short_id, short_url=short_url)


@router.get("/{short_id}")
async def redirect_to_original(
    short_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Редиректит на оригинальную ссылку + увеличивает счётчик"""
    
    
    link = await crud.get_link_by_short_id(db, short_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    
    await crud.increment_clicks(db, short_id)
    

    return RedirectResponse(url=link.original_url)


@router.get("/stats/{short_id}", response_model=schemas.StatsResponse)
async def get_link_stats(
    short_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Возвращает статистику переходов по ссылке"""
    
    clicks = await crud.get_stats(db, short_id)
    if clicks is None:
        raise HTTPException(status_code=404, detail="Link not found")
    
    return schemas.StatsResponse(short_id=short_id, clicks=clicks)