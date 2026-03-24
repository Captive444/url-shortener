from pydantic import BaseModel, HttpUrl


class LinkCreate(BaseModel):
    """Схема для создания ссылки (POST /shorten)"""
    url: HttpUrl  


class LinkResponse(BaseModel):
    """Схема ответа при создании ссылки"""
    short_id: str
    short_url: str  


class StatsResponse(BaseModel):
  
    short_id: str
    clicks: int