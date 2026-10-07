"""
Authoritative Database Session & Engine Configuration for Astrovision.
Supports SQLite persistent storage for development/testing and PostgreSQL for production via DATABASE_URL.
"""
import os
import logging
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from apps.api.config import settings

logger = logging.getLogger("astrovision.db")

def get_database_url() -> str:
    """Resolves database URL from environment or settings."""
    return os.environ.get("DATABASE_URL", settings.database_url or "sqlite:///./astrovision.db")

def create_db_engine():
    """Creates SQLAlchemy engine with dialect-specific connection pooling."""
    db_url = get_database_url()

    if db_url.startswith("sqlite"):
        return create_engine(
            db_url,
            connect_args={"check_same_thread": False},
            echo=False
        )
    else:
        # PostgreSQL / Server Relational Database
        return create_engine(
            db_url,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_pre_ping=True,
            echo=False
        )

engine = create_db_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db() -> None:
    """Initializes all database tables in persistent storage."""
    try:
        from apps.api.db.models import (
            UserModel,
            BirthProfileModel,
            CalculationReportModel,
            AIInterpretationRecordModel,
            SavedChartModel,
            AuditRecordModel
        )
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise

def get_db() -> Generator[Session, None, None]:
    """Dependency for providing a transactional database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_database_status() -> str:
    """Returns real operational status of the persistent database."""
    try:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_url = get_database_url()
        if db_url.startswith("sqlite"):
            return "sqlite_persistent"
        return "postgresql_persistent"
    except Exception as e:
        return f"database_error: {str(e)}"
