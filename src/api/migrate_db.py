import os

from sqlalchemy import create_engine

from src.api.models.task import Base

DB_USER = os.environ.get("DB_USER", "dev")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "dev")
DB_HOST = os.environ.get("DB_HOST", "db")
DB_NAME = os.environ.get("DB_NAME", "devdb")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
print(DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=True)

def migrate_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    migrate_db()
