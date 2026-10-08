"""
Audit Logging Helper Module for Astrovision.
Logs security-sensitive actions to AuditRecordModel in database without logging sensitive secrets.
"""
import json
from typing import Optional
from sqlalchemy.orm import Session
from apps.api.db.models import AuditRecordModel

def record_audit_event(
    db: Session,
    user_id: str,
    action: str,
    endpoint: str,
    ip_address: Optional[str] = None,
    details: Optional[dict] = None
) -> AuditRecordModel:
    """
    Creates an immutable audit record in the database for security auditing.
    Never logs plain passwords or raw JWT secret keys.
    """
    safe_details = {}
    if details:
        for k, v in details.items():
            if k.lower() in ["password", "token", "jwt", "secret", "hashed_password"]:
                safe_details[k] = "[REDACTED]"
            else:
                safe_details[k] = v

    record = AuditRecordModel(
        user_id=user_id,
        action=action,
        endpoint=endpoint,
        ip_address=ip_address,
        details_json=json.dumps(safe_details)
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record
