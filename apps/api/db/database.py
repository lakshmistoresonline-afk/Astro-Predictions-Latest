"""
Authoritative Database Session & Engine Configuration for Astrovision.
Supports SQLite persistent storage (default astrovision.db) and PostgreSQL via DATABASE_URL.
"""
import os
import logging
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

logger = logging.getLogger("astrovision.db")

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./astrovision.db")

connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    pool_pre_ping=True
)

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
        if DATABASE_URL.startswith("sqlite"):
            return "sqlite_persistent"
        return "postgresql_persistent"
    except Exception as e:
        return f"database_error: {str(e)}"
