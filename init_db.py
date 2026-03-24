import asyncio
from app.database import engine, Base
from app.models import Link 


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # удаляем табл
        await conn.run_sync(Base.metadata.create_all)  
    print("Database initialized!")


if __name__ == "__main__":
    asyncio.run(init())