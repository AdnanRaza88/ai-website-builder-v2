from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    from core import models  # noqa
    Base.metadata.create_all(bind=engine)
