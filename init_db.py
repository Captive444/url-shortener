import os
import asyncio
from app.database import engine, Base


async def init():
    os.makedirs("data", exist_ok=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database initialized!!!!")


if __name__ == "__main__":
    asyncio.run(init())