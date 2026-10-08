"""
User Feedback and Calculation Correction Reporting Router for Astrovision.
Allows authenticated pilot users to submit feedback and report calculation discrepancies cleanly.
"""
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional

from apps.api.db.database import get_db
from apps.api.db.models import UserModel
from apps.api.db.auth import get_current_user
from apps.api.db.audit import record_audit_event

router = APIRouter(prefix="/api/v1/feedback", tags=["User Feedback"])

class FeedbackSubmitRequest(BaseModel):
    category: str = Field(description="Bug, CalculationDiscrepancy, UIProblem, Performance, FeatureRequest, Other")
    message: str = Field(min_length=5, max_length=2000, description="Feedback description")
    master_evidence_hash: Optional[str] = Field(default=None, description="Optional calculation evidence hash for investigation")
    calculation_report_id: Optional[str] = Field(default=None, description="Optional report ID for calculation discrepancy reports")

@router.post("", status_code=status.HTTP_201_CREATED)
def submit_user_feedback(
    req: FeedbackSubmitRequest,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Submits user feedback or calculation discrepancy report for investigation."""
    record = record_audit_event(
        db=db,
        user_id=current_user.id,
        action=f"FEEDBACK_{req.category.upper()}",
        endpoint="/api/v1/feedback",
        details={
            "category": req.category,
            "message_snippet": req.message[:100],
            "master_evidence_hash": req.master_evidence_hash,
            "calculation_report_id": req.calculation_report_id
        }
    )

    return {
        "status": "received",
        "feedback_id": record.id,
        "message": "Thank you! Your feedback has been recorded for pilot investigation."
    }
