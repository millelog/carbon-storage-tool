from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings


if settings.DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set")

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session