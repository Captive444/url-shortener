from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс для настроек приложения.

    Содержит настройки для бд, базового URL и длины короткого идентификатора.
    """
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/url_shortener"
    BASE_URL: str = "http://localhost:8000"
    SHORT_ID_LENGTH: int = 6  

    class Config:
        env_file = ".env"


settings = Settings()
