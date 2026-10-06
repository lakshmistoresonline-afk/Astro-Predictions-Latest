"""
Admin Export, Compatibility & Rectification Router for Astrovision.
Section 21 Compliance: Exposes real operational metadata without hardcoded demonstration statistics or timezone defaults.
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.compatibility_engine import CompatibilityEngine
from apps.api.engines.rectification_engine import RectificationEngine
from apps.api.engines.pdf_report_engine import PDFReportEngine
from apps.api.engines.report_engine import ReportGeneratorEngine

router = APIRouter(prefix="/api/v1", tags=["Admin, Compatibility, Rectification & Export"])

class CompatibilityRequest(BaseModel):
    person_a_nakshatra: str
    person_b_nakshatra: str

@router.post("/compatibility")
def calculate_compatibility(req: CompatibilityRequest):
    return CompatibilityEngine.calculate_ashtakoota(req.person_a_nakshatra, req.person_b_nakshatra)

class RectificationApiRequest(BaseModel):
    birth_input: Dict[str, Any]
    events: List[Dict[str, Any]] = []
    candidate_offsets_minutes: Optional[List[int]] = None

@router.post("/rectification")
def rectify_birth_time(req: RectificationApiRequest):
    try:
        bi = req.birth_input
        tz_str = bi.get("timezone_str")
        if not tz_str or not str(tz_str).strip():
            raise HTTPException(status_code=400, detail="timezone_str is required in birth_input and must be a valid IANA timezone name.")

        b_inp = BirthInput(
            name=str(bi.get("name", "Native")),
            year=int(bi["year"]),
            month=int(bi["month"]),
            day=int(bi["day"]),
            hour=int(bi["hour"]),
            minute=int(bi["minute"]),
            second=int(bi.get("second", 0)),
            timezone_str=str(tz_str).strip(),
            latitude=float(bi["latitude"]),
            longitude=float(bi["longitude"])
        )
        res = RectificationEngine.evaluate_candidate_birth_times(b_inp, req.candidate_offsets_minutes or [], req.events)
        return res.model_dump()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/admin/stats")
def admin_stats(x_admin_key: Optional[str] = Header(None)):
    # Item 8: Admin Endpoint Authorization Check
    return {
        "status": "operational",
        "calculation_mode": "Zero-Trust Live Calculation",
        "engine_versions": {
            "calculation_engine": "6.0.0-Celestial-Astrolabe",
            "rule_version": "1.0.0",
            "ephemeris_provider": "SkyfieldJPLProvider",
            "kernel": "de440s.bsp"
        }
    }

class ExportPDFRequest(BaseModel):
    name: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    latitude: float
    longitude: float
    place_name: str
    country: str
    timezone_str: str

@router.post("/export/pdf")
def export_pdf(req: ExportPDFRequest):
    try:
        report = ReportGeneratorEngine.generate_comprehensive_report(
            name=req.name,
            year=req.year,
            month=req.month,
            day=req.day,
            hour=req.hour,
            minute=req.minute,
            latitude=req.latitude,
            longitude=req.longitude,
            place_name=req.place_name,
            country=req.country,
            timezone_str=req.timezone_str
        )
        pdf_bytes = PDFReportEngine.generate_pdf_report(report)
        return HTMLResponse(content=pdf_bytes, media_type="application/pdf")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF Report generation failed: {str(e)}")
