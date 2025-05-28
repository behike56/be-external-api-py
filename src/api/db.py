import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DB_USER = os.environ.get("DB_USER", "dev")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "dev")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "devdb")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

db_engine = create_async_engine(DATABASE_URL, echo=True)
db_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=db_engine,
    class_=AsyncSession,
)

Base = declarative_base()


async def get_db():
    async with db_session() as session:
        yield session
