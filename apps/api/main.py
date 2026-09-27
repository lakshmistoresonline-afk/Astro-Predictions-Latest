from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from apps.api.config import settings
from apps.api.engines.birth_engine import BirthDataEngine
from apps.api.engines.report_engine import ReportGeneratorEngine
from apps.api.engines.svg_chart_engine import SVGChartEngine
from apps.api.services.ai_service import AIService
from apps.api.routers.admin_export import router as admin_export_router

app = FastAPI(
    title=settings.app_name,
    version="6.0.0",
    description="Deterministic Astrology Computation and Prediction Platform"
)

# Production-safe explicit CORS configuration (Part 2, Item 11 & Part 32)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://astrovision.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_export_router)

class BirthProfileRequest(BaseModel):
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
    birth_time_accuracy: Optional[str] = "exact"
    zodiac_system: Optional[str] = "sidereal"
    ayanamsha: Optional[str] = "lahiri"

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "api_status": "active",
        "database_status": "connected",
        "ephemeris_status": "available",
        "ai_model_generation": settings.ai_model_generation,
        "ai_model_validation": settings.ai_model_validation,
        "engine_version": "6.0.0-Celestial-Astrolabe"
    }

@app.get("/ready")
def readiness_check():
    return {"ready": True}

@app.get("/version")
def version_info():
    return {
        "version": "6.0.0",
        "engine_version": "6.0.0-Celestial-Astrolabe",
        "rule_version": "1.0.0",
        "ephemeris_version": "Meeus-Astronomical-Algorithms-2.10"
    }

@app.post("/api/v1/birth-profile")
def calculate_birth_profile(req: BirthProfileRequest):
    try:
        birth_data = BirthDataEngine.process_birth_data(
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
            birth_time_accuracy=req.birth_time_accuracy
        )

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
            zodiac_system=req.zodiac_system or "sidereal",
            ayanamsha=req.ayanamsha or "lahiri"
        )

        svg_wheel = SVGChartEngine.generate_circular_zodiac_wheel(report["chapter_3_planetary_positions"]["data"], "NATAL ZODIAC ASTROLABE (D1)")

        navamsa_pos = {}
        for p, v in report["chapter_6_divisional_charts"]["data"].items():
            sign_map = {"Aries": 15, "Taurus": 45, "Gemini": 75, "Cancer": 105, "Leo": 135, "Virgo": 165, "Libra": 195, "Scorpio": 225, "Sagittarius": 255, "Capricorn": 285, "Aquarius": 315, "Pisces": 345}
            s = v.get("D9_Navamsa", "Aries")
            navamsa_pos[p] = {"sign": s, "longitude": sign_map.get(s, 0)}

        svg_navamsa_wheel = SVGChartEngine.generate_circular_zodiac_wheel(navamsa_pos, "NAVAMSA ASTROLABE (D9)")

        return {
            "birth_profile": birth_data,
            "planetary_positions": report["chapter_3_planetary_positions"]["data"],
            "vedic_analysis": report["chapter_3_planetary_positions"]["data"],
            "western_aspects": [],
            "dasha_info": report["chapter_8_dasha"]["data"],
            "divisional_charts": report["chapter_6_divisional_charts"]["data"],
            "yogas": report["chapter_7_yogas"]["data"],
            "predictions": report["chapter_9_life_domains"]["data"],
            "svg_chart": svg_wheel,
            "svg_navamsa": svg_navamsa_wheel,
            "complete_report": report
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Calculation Error: {str(e)}"
        )

class AIInterpretRequest(BaseModel):
    prompt: str
    evidence: dict

@app.post("/api/v1/ai/interpret")
def ai_interpret(req: AIInterpretRequest):
    interpretation = AIService.generate_interpretation(req.prompt, req.evidence)
    validation = AIService.validate_interpretation(interpretation, req.evidence)
    return {
        "interpretation": interpretation,
        "validation_status": validation
    }
