from sqlalchemy import Column, Integer, String, DateTime, Index, CheckConstraint
from sqlalchemy.sql import func
from .database import Base


class Link(Base):
    """
    Модель для хранения коротких ссылок
    
    TODO: добавить поле user_id если понадобится авторизация
    TODO: добавить поле expires_at для временных ссылок
    TODO: добавить поле is_active для мягкого удаления
    """
    __tablename__ = "links"
    
  
    id = Column(Integer, primary_key=True, index=True, comment="Внутренний ID")
    
 
    original_url = Column(
        String(2048),  
        nullable=False,
        comment="Оригинальный URL (максимум. 2048 символов)"
    )
    short_id = Column(
        String(32),  
        unique=True, 
        index=True, 
        nullable=False,
        comment="Уникальный идентификатор короткой ссылки"
    )
    
    # Статист
    clicks = Column(
        Integer, 
        default=0, 
        nullable=False,
        comment="Количество переходов по ссылке"
    )
    
    # время 
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        comment="Дата создания ссылки"
    )
    
    # TODO: добавить updated_at для отслеживания изменений
    # updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Составные индексы для оптимизации запросов
    # TODO: добавить индекс на created_at для сортировки по дате
    __table_args__ = (
        Index('ix_links_created_at', created_at),
        # Проверка short_id на пустоту
        CheckConstraint('short_id != ""', name='check_short_id_not_empty'),
        CheckConstraint('original_url != ""', name='check_original_url_not_empty'),
        # TODO: добавить уникальность на original_url
        # UniqueConstraint('original_url', name='uq_links_original_url'),
        {'comment': 'Таблица с короткими ссылками'}
    )
    
    def __repr__(self) -> str:
        
        return f"<Link(id={self.id}, short_id={self.short_id}, clicks={self.clicks})>"
    
    def increment_clicks(self) -> None:
        """Увеличивает счётчик кликов - для бизнес-логики"""
        self.clicks += 1

