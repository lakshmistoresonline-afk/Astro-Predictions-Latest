"""
Test Suite for Audit Logging & Security Event Recording.
"""
import pytest
import json
from apps.api.db.database import init_db, SessionLocal
from apps.api.db.audit import record_audit_event
from apps.api.db.models import AuditRecordModel

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

def test_audit_event_recording_redacts_secrets():
    """Verifies that audit logging records security events while redacting passwords and secret keys."""
    db = SessionLocal()
    user_id = "user_audit_test_123"

    record = record_audit_event(
        db=db,
        user_id=user_id,
        action="USER_LOGIN",
        endpoint="/api/v1/auth/login",
        ip_address="127.0.0.1",
        details={
            "email": "audit_user@astrovision.test",
            "password": "SuperSecretPassword123!",
            "token": "secret_bearer_token"
        }
    )

    assert record.id is not None
    assert record.action == "USER_LOGIN"
    assert record.user_id == user_id

    details = json.loads(record.details_json)
    assert details["email"] == "audit_user@astrovision.test"
    assert details["password"] == "[REDACTED]"
    assert details["token"] == "[REDACTED]"

    db.close()
