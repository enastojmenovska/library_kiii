from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

def check_db_connection() -> None:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

def init_db() -> None:
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
