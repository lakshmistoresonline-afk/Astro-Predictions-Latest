"""
Test Suite for Quota Governance, Persistent Rate Limiting, and User Isolation.
"""
import pytest
from fastapi.testclient import TestClient
from apps.api.main import app
from apps.api.config import settings
from apps.api.db.database import init_db, SessionLocal
from apps.api.services.quota_service import QuotaGovernanceService, QuotaExceededException

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

def test_chart_quota_enforcement():
    """Verifies daily chart quota enforcement for user."""
    db = SessionLocal()
    user_id = "user_quota_test_001"

    # Consume up to limit
    limit = settings.free_daily_charts
    for _ in range(limit):
        QuotaGovernanceService.check_and_increment_chart_quota(db, user_id)

    # Next request over limit raises QuotaExceededException (HTTP 429)
    with pytest.raises(QuotaExceededException):
        QuotaGovernanceService.check_and_increment_chart_quota(db, user_id)

    db.close()

def test_user_quota_isolation():
    """Verifies that User A's quota consumption does NOT affect User B."""
    db = SessionLocal()
    user_a = "user_quota_isolation_A"
    user_b = "user_quota_isolation_B"

    # User A consumes all quota
    limit = settings.free_daily_charts
    for _ in range(limit):
        QuotaGovernanceService.check_and_increment_chart_quota(db, user_a)

    # User A is blocked
    with pytest.raises(QuotaExceededException):
        QuotaGovernanceService.check_and_increment_chart_quota(db, user_a)

    # User B is NOT blocked and has full quota available
    remaining = QuotaGovernanceService.check_and_increment_chart_quota(db, user_b)
    assert remaining == limit - 1

    db.close()
