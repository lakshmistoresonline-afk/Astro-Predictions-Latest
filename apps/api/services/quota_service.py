"""
Quota Governance and Usage Limit Enforcement Service for Astrovision.
Enforces daily free-tier limits: charts_calculated, ai_reports_generated, ai_messages_sent.
"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from apps.api.config import settings
from apps.api.db.models import UserQuotaModel

class QuotaExceededException(HTTPException):
    def __init__(self, resource_type: str, limit: int):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": f"Daily free-tier quota exceeded for {resource_type}. Limit: {limit}.",
                "error_code": "QUOTA_EXCEEDED",
                "resource_type": resource_type,
                "daily_limit": limit,
                "remaining_quota": 0
            }
        )

class QuotaGovernanceService:

    @classmethod
    def get_today_utc_str(cls) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")

    @classmethod
    def get_or_create_quota_record(cls, db: Session, identifier: str) -> UserQuotaModel:
        today = cls.get_today_utc_str()
        quota = db.query(UserQuotaModel).filter(
            UserQuotaModel.identifier == identifier,
            UserQuotaModel.usage_date == today
        ).first()

        if not quota:
            quota = UserQuotaModel(
                identifier=identifier,
                usage_date=today,
                charts_calculated=0,
                ai_reports_generated=0,
                ai_messages_sent=0
            )
            db.add(quota)
            db.commit()
            db.refresh(quota)

        return quota

    @classmethod
    def check_and_increment_chart_quota(cls, db: Session, identifier: str) -> int:
        quota = cls.get_or_create_quota_record(db, identifier)
        limit = settings.free_daily_charts

        if quota.charts_calculated >= limit:
            raise QuotaExceededException("charts_calculated", limit)

        quota.charts_calculated += 1
        db.commit()
        return limit - quota.charts_calculated

    @classmethod
    def check_and_increment_ai_message_quota(cls, db: Session, identifier: str) -> int:
        quota = cls.get_or_create_quota_record(db, identifier)
        limit = settings.free_daily_ai_messages

        if quota.ai_messages_sent >= limit:
            raise QuotaExceededException("ai_messages_sent", limit)

        quota.ai_messages_sent += 1
        db.commit()
        return limit - quota.ai_messages_sent
