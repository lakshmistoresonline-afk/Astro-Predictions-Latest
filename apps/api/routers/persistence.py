"""
Persistent User Resources Router for Astrovision.
Section 1..13 Compliance:
- Server-enforced user ownership on every read, update, delete operation.
- Server NEVER trusts client-supplied owner IDs!
- Server-enforced IDOR protection across profiles, reports, saved charts, and PDF exports.
"""
import json
import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from apps.api.db.database import get_db
from apps.api.db.models import (
    UserModel,
    BirthProfileModel,
    CalculationReportModel,
    SavedChartModel,
    AIInterpretationRecordModel,
    AuditRecordModel
)
from apps.api.db.auth import get_current_user
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.canonical_evidence import CanonicalEvidencePipeline
from apps.api.engines.prediction_engine import PredictionEngine
from apps.api.engines.svg_chart_engine import SVGChartEngine
from apps.api.engines.report_engine import ReportGeneratorEngine
from apps.api.engines.pdf_report_engine import PDFReportEngine

logger = logging.getLogger("astrovision.persistence")

router = APIRouter(prefix="/api/v1", tags=["Persistence & User Resources"])

class BirthProfileCreateRequest(BaseModel):
    name: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int = 0
    timezone_str: str
    latitude: float
    longitude: float
    place_name: str
    country: str

class SavedChartCreateRequest(BaseModel):
    birth_profile_id: str
    chart_title: str
    notes: Optional[str] = None

@router.post("/profiles", status_code=status.HTTP_201_CREATED)
def create_profile(
    req: BirthProfileCreateRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Creates a persistent birth profile owned by the authenticated user."""
    profile = BirthProfileModel(
        user_id=current_user.id,
        name=req.name,
        year=req.year,
        month=req.month,
        day=req.day,
        hour=req.hour,
        minute=req.minute,
        second=req.second,
        timezone_str=req.timezone_str,
        latitude=req.latitude,
        longitude=req.longitude,
        place_name=req.place_name,
        country=req.country
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    # Audit Record
    audit = AuditRecordModel(
        user_id=current_user.id,
        action="CREATE_PROFILE",
        endpoint="/api/v1/profiles",
        details_json=json.dumps({"profile_id": profile.id, "name": req.name})
    )
    db.add(audit)
    db.commit()

    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "name": profile.name,
        "year": profile.year,
        "month": profile.month,
        "day": profile.day,
        "hour": profile.hour,
        "minute": profile.minute,
        "second": profile.second,
        "timezone_str": profile.timezone_str,
        "latitude": profile.latitude,
        "longitude": profile.longitude,
        "place_name": profile.place_name,
        "country": profile.country,
        "created_at": profile.created_at.isoformat()
    }

@router.get("/profiles")
def list_profiles(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lists all birth profiles owned strictly by the authenticated user."""
    profiles = db.query(BirthProfileModel).filter(BirthProfileModel.user_id == current_user.id).all()
    return [
        {
            "id": p.id,
            "user_id": p.user_id,
            "name": p.name,
            "year": p.year,
            "month": p.month,
            "day": p.day,
            "hour": p.hour,
            "minute": p.minute,
            "timezone_str": p.timezone_str,
            "latitude": p.latitude,
            "longitude": p.longitude,
            "place_name": p.place_name,
            "country": p.country,
            "created_at": p.created_at.isoformat()
        } for p in profiles
    ]

@router.get("/profiles/{profile_id}")
def get_profile(
    profile_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves a birth profile owned strictly by current_user. Enforces server-side IDOR check!"""
    profile = db.query(BirthProfileModel).filter(
        BirthProfileModel.id == profile_id,
        BirthProfileModel.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Birth profile '{profile_id}' not found or access denied."
        )

    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "name": profile.name,
        "year": profile.year,
        "month": profile.month,
        "day": profile.day,
        "hour": profile.hour,
        "minute": profile.minute,
        "timezone_str": profile.timezone_str,
        "latitude": profile.latitude,
        "longitude": profile.longitude,
        "place_name": profile.place_name,
        "country": profile.country,
        "created_at": profile.created_at.isoformat()
    }

@router.put("/profiles/{profile_id}")
def update_profile(
    profile_id: str,
    req: BirthProfileCreateRequest,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Updates a birth profile owned strictly by current_user. Enforces server-side IDOR check!"""
    profile = db.query(BirthProfileModel).filter(
        BirthProfileModel.id == profile_id,
        BirthProfileModel.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Birth profile '{profile_id}' not found or access denied."
        )

    profile.name = req.name
    profile.year = req.year
    profile.month = req.month
    profile.day = req.day
    profile.hour = req.hour
    profile.minute = req.minute
    profile.second = req.second
    profile.timezone_str = req.timezone_str
    profile.latitude = req.latitude
    profile.longitude = req.longitude
    profile.place_name = req.place_name
    profile.country = req.country

    db.commit()
    db.refresh(profile)

    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "name": profile.name,
        "updated_at": profile.created_at.isoformat()
    }

@router.delete("/profiles/{profile_id}")
def delete_profile(
    profile_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deletes a birth profile owned strictly by current_user. Enforces server-side IDOR check!"""
    profile = db.query(BirthProfileModel).filter(
        BirthProfileModel.id == profile_id,
        BirthProfileModel.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Birth profile '{profile_id}' not found or access denied."
        )

    db.delete(profile)
    db.commit()

    return {"status": "deleted", "id": profile_id}

@router.post("/reports", status_code=status.HTTP_201_CREATED)
def calculate_and_save_report(
    profile_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Calculates and saves a persistent report for a user's profile. Enforces server-side IDOR check!"""
    profile = db.query(BirthProfileModel).filter(
        BirthProfileModel.id == profile_id,
        BirthProfileModel.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Birth profile '{profile_id}' not found or access denied."
        )

    b_inp = BirthInput(
        name=profile.name,
        year=profile.year,
        month=profile.month,
        day=profile.day,
        hour=profile.hour,
        minute=profile.minute,
        second=profile.second,
        timezone_str=profile.timezone_str,
        latitude=profile.latitude,
        longitude=profile.longitude
    )

    master_evidence = CanonicalEvidencePipeline.generate_canonical_evidence(b_inp)
    prediction_package = PredictionEngine.generate_all_predictions(master_evidence)
    svg_chart = SVGChartEngine.generate_north_indian_chart(master_evidence.canonical_chart)
    report_dict = ReportGeneratorEngine.generate_comprehensive_report(
        name=profile.name,
        year=profile.year,
        month=profile.month,
        day=profile.day,
        hour=profile.hour,
        minute=profile.minute,
        latitude=profile.latitude,
        longitude=profile.longitude,
        place_name=profile.place_name,
        country=profile.country,
        timezone_str=profile.timezone_str
    )

    report_record = CalculationReportModel(
        user_id=current_user.id,
        birth_profile_id=profile.id,
        chart_hash=master_evidence.master_evidence_hash,
        master_evidence_json=json.dumps(master_evidence.model_dump()),
        predictions_json=json.dumps(prediction_package.model_dump()),
        svg_chart=svg_chart,
        report_json=json.dumps(report_dict)
    )
    db.add(report_record)
    db.commit()
    db.refresh(report_record)

    return {
        "id": report_record.id,
        "user_id": report_record.user_id,
        "birth_profile_id": report_record.birth_profile_id,
        "chart_hash": report_record.chart_hash,
        "created_at": report_record.created_at.isoformat()
    }

@router.get("/reports/{report_id}")
def get_report(
    report_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves a calculation report owned strictly by current_user. Enforces server-side IDOR check!"""
    report_record = db.query(CalculationReportModel).filter(
        CalculationReportModel.id == report_id,
        CalculationReportModel.user_id == current_user.id
    ).first()

    if not report_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report '{report_id}' not found or access denied."
        )

    return {
        "id": report_record.id,
        "user_id": report_record.user_id,
        "birth_profile_id": report_record.birth_profile_id,
        "chart_hash": report_record.chart_hash,
        "master_evidence": json.loads(report_record.master_evidence_json),
        "predictions": json.loads(report_record.predictions_json),
        "svg_chart": report_record.svg_chart,
        "report": json.loads(report_record.report_json) if report_record.report_json else None,
        "created_at": report_record.created_at.isoformat()
    }

@router.get("/reports/{report_id}/pdf")
def export_report_pdf(
    report_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Exports PDF report owned strictly by current_user. Enforces server-side IDOR check!"""
    report_record = db.query(CalculationReportModel).filter(
        CalculationReportModel.id == report_id,
        CalculationReportModel.user_id == current_user.id
    ).first()

    if not report_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report '{report_id}' not found or access denied."
        )

    report_dict = json.loads(report_record.report_json)
    pdf_bytes = PDFReportEngine.generate_pdf_report(report_dict)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="astrovision_report.pdf"'}
    )
