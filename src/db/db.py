from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings

engine = create_async_engine(settings.POSTGRESQL_DB_URL)

SessionLocal = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
