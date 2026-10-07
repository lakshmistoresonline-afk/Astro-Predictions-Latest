"""
SQLAlchemy Persistent ORM Models for Astrovision.
Section 1..13 Compliance: Explicit user_id foreign keys, indexes, and user ownership models.
"""
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from apps.api.db.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utc_now() -> datetime:
    return datetime.now(timezone.utc)

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    password_salt = Column(String(64), nullable=True)
    full_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    birth_profiles = relationship("BirthProfileModel", back_populates="owner", cascade="all, delete-orphan")
    calculation_reports = relationship("CalculationReportModel", back_populates="owner", cascade="all, delete-orphan")
    saved_charts = relationship("SavedChartModel", back_populates="owner", cascade="all, delete-orphan")

class BirthProfileModel(Base):
    __tablename__ = "birth_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    hour = Column(Integer, nullable=False)
    minute = Column(Integer, nullable=False)
    second = Column(Integer, default=0, nullable=False)
    timezone_str = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    place_name = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    created_at = Column(DateTime, default_utc_now, nullable=False)

    owner = relationship("UserModel", back_populates="birth_profiles")
    reports = relationship("CalculationReportModel", back_populates="birth_profile", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_birth_profiles_user_id_id", "user_id", "id"),
    )

class CalculationReportModel(Base):
    __tablename__ = "calculation_reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    birth_profile_id = Column(String(36), ForeignKey("birth_profiles.id"), nullable=False, index=True)
    chart_hash = Column(String(64), nullable=False, index=True)
    master_evidence_json = Column(Text, nullable=False)
    predictions_json = Column(Text, nullable=False)
    svg_chart = Column(Text, nullable=True)
    report_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default_utc_now, nullable=False)

    owner = relationship("UserModel", back_populates="calculation_reports")
    birth_profile = relationship("BirthProfileModel", back_populates="reports")
    ai_interpretations = relationship("AIInterpretationRecordModel", back_populates="report", cascade="all, delete-orphan")

    __table_args__ = (
        Index("ix_reports_user_id_id", "user_id", "id"),
    )

class AIInterpretationRecordModel(Base):
    __tablename__ = "ai_interpretations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    calculation_report_id = Column(String(36), ForeignKey("calculation_reports.id"), nullable=False, index=True)
    domain = Column(String(50), nullable=False, index=True)
    prompt = Column(Text, nullable=False)
    interpretation_text = Column(Text, nullable=False)
    validation_status = Column(String(50), nullable=False)
    created_at = Column(DateTime, default_utc_now, nullable=False)

    report = relationship("CalculationReportModel", back_populates="ai_interpretations")

class SavedChartModel(Base):
    __tablename__ = "saved_charts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    birth_profile_id = Column(String(36), ForeignKey("birth_profiles.id"), nullable=False, index=True)
    chart_title = Column(String(255), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    owner = relationship("UserModel", back_populates="saved_charts")

class AuditRecordModel(Base):
    __tablename__ = "audit_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), nullable=False, index=True)
    action = Column(String(100), nullable=False, index=True)
    endpoint = Column(String(255), nullable=False)
    ip_address = Column(String(50), nullable=True)
    details_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default_utc_now, nullable=False)
