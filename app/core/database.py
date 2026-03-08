from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


engine = create_engine(settings.sqlalchemy_database_uri, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app.models.device import Device  # noqa: F401
    from app.models.device_status import DeviceStatus  # noqa: F401

    Base.metadata.create_all(bind=engine)
