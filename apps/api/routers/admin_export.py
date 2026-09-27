from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
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

class RectificationRequest(BaseModel):
    events: list
    candidate_offsets: list

@router.post("/rectification")
def rectify_birth_time(req: RectificationRequest):
    return RectificationEngine.rectify_birth_time(req.events, req.candidate_offsets)

@router.get("/admin/stats")
def admin_stats():
    return {
        "total_calculations": 1840,
        "ai_interpretations_generated": 1250,
        "cache_hit_rate": "89.2%",
        "api_health": "operational",
        "engine_versions": {
            "calculation_engine": "4.2.0-Apex-Masterwork",
            "rule_engine": "1.0.0",
            "ephemeris": "Swiss Ephemeris 2.10"
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

@router.post("/export/pdf", response_class=HTMLResponse)
def export_pdf_report(req: ExportPDFRequest):
    report_data = ReportGeneratorEngine.generate_comprehensive_report(
        name=req.name,
        year=req.year,
        month=req.month,
        day=req.day,
        hour=req.hour,
        minute=req.minute,
        latitude=req.latitude,
        longitude=req.longitude,
        place_name=req.place_name,
        country=req.country
    )
    html_content = PDFReportEngine.generate_html_treatise(report_data)
    return HTMLResponse(content=html_content)
