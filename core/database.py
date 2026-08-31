from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_conn, connection_record):
    if "sqlite" in settings.DATABASE_URL:
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def init_db(force_reset: bool = True):
    """Create tables. force_reset=True drops existing tables first (dev only)."""
    from core import models  # noqa: F401
    if force_reset and "sqlite" in settings.DATABASE_URL:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
