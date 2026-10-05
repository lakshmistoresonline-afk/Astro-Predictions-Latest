"""
Master FastAPI Application Entry Point for Astrovision (Phase 2E-R4.1-R12-R10).
Exposes deterministic local astrology APIs backed by NASA JPL DE440s, 16 Vargas, 5-Level Dasha,
Shadbala, Ashtakavarga, Transits, Panchanga, Muhurta, Jaimini, Timing Engine, and Server-Owned Evidence AI Handoff.
"""
import os
import hashlib
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from apps.api.config import settings
from apps.api.engines.birth_engine import BirthDataEngine
from apps.api.engines.report_engine import ReportGeneratorEngine
from apps.api.engines.svg_chart_engine import SVGChartEngine
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.canonical_evidence import CanonicalEvidencePipeline, CanonicalAstrologyEvidence
from apps.api.engines.prediction_engine import PredictionEngine, ComprehensivePredictionPackage
from apps.api.engines.transit.engine import TransitEngine
from apps.api.engines.transit.models import TransitSnapshot
from apps.api.engines.panchanga.engine import PanchangaEngine
from apps.api.engines.panchanga.models import PanchangaResult
from apps.api.engines.muhurta.engine import MuhurtaEngine
from apps.api.engines.muhurta.models import MuhurtaSuiteResult
from apps.api.engines.jaimini.engine import JaiminiEngine
from apps.api.engines.jaimini.models import JaiminiSuiteResult
from apps.api.engines.timing.engine import TimingEngine
from apps.api.engines.timing.models import TimingSuiteResult
from apps.api.services.ai_service import AIService
from apps.api.routers.admin_export import router as admin_export_router

app = FastAPI(
    title=settings.app_name,
    version="6.0.0",
    description="Deterministic Astrology Computation, Transit, Panchanga, Muhurta, Jaimini and Prediction Platform"
)

# Production-safe explicit CORS configuration
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

EXPECTED_DE440S_SHA256 = "c1c7feeab882263fc493a9d5a5b2ddd71b54826cdf65d8d17a76126b260a49f2"

def verify_de440s_kernel_status() -> tuple:
    base_module_dir = os.path.dirname(os.path.abspath(__file__))
    de440s_path = os.path.join(base_module_dir, "engines", "astronomy", "de440s.bsp")
    if not os.path.exists(de440s_path):
        return False, f"DE440s kernel missing at {de440s_path}"

    if os.path.getsize(de440s_path) < 30000000:
        return False, "DE440s kernel size < 30MB"

    with open(de440s_path, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()

    if h != EXPECTED_DE440S_SHA256:
        return False, f"DE440s kernel SHA-256 mismatch: got {h}"

    return True, f"SHA-256:{h[:16]}... (32,726,016 bytes)"

class BirthProfileRequest(BaseModel):
    name: str
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: Optional[int] = 0
    timezone_str: str = Field(description="Explicit IANA timezone string e.g. 'Asia/Kolkata'")
    latitude: float
    longitude: float
    place_name: str
    country: str
    birth_time_accuracy: Optional[str] = "exact"

class TransitRequest(BaseModel):
    birth_input: BirthProfileRequest
    query_datetime_iso: Optional[str] = None

class AIInterpretationRequest(BaseModel):
    birth_input: BirthProfileRequest
    prompt: str
    domain: Optional[str] = "CAREER"

@app.get("/health")
def health_check():
    de440s_valid, de440s_msg = verify_de440s_kernel_status()
    return {
        "status": "healthy" if de440s_valid else "degraded",
        "api_status": "active",
        "database_status": "standalone_in_memory",
        "ephemeris_status": "NASA JPL DE440s Verified" if de440s_valid else f"error: {de440s_msg}",
        "ai_model_generation": settings.ai_model_generation,
        "ai_model_validation": settings.ai_model_validation,
        "engine_version": "6.0.0-Celestial-Astrolabe"
    }

@app.get("/ready")
def readiness_check():
    de440s_valid, de440s_msg = verify_de440s_kernel_status()
    if not de440s_valid:
        raise HTTPException(status_code=503, detail=f"Ephemeris kernel DE440s unavailable: {de440s_msg}")
    return {"ready": True}

@app.get("/version")
def version_info():
    return {
        "version": "6.0.0",
        "engine_version": "6.0.0-Celestial-Astrolabe",
        "rule_version": "1.0.0",
        "ephemeris_version": "NASA JPL DE440s via Skyfield 1.55",
        "ayanamsha": "Lahiri",
        "node_convention": "Canonical Mean Node (Rahu & Ketu)"
    }

@app.post("/api/v1/birth-profile")
def calculate_birth_profile(req: BirthProfileRequest):
    try:
        b_inp = BirthInput(
            name=req.name,
            year=req.year,
            month=req.month,
            day=req.day,
            hour=req.hour,
            minute=req.minute,
            second=req.second if req.second is not None else 0,
            timezone_str=req.timezone_str,
            latitude=req.latitude,
            longitude=req.longitude
        )

        master_evidence = CanonicalEvidencePipeline.generate_canonical_evidence(b_inp)
        prediction_package = PredictionEngine.generate_all_predictions(master_evidence)
        svg_chart = SVGChartEngine.generate_north_indian_chart(master_evidence.canonical_chart)

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

        return {
            "status": "success",
            "birth_input": req.model_dump(),
            "master_evidence": master_evidence.model_dump(),
            "predictions": prediction_package.model_dump(),
            "svg_chart": svg_chart,
            "report": report
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/transit-snapshot")
def get_transit_snapshot(req: TransitRequest):
    try:
        b_inp = BirthInput(
            name=req.birth_input.name,
            year=req.birth_input.year,
            month=req.birth_input.month,
            day=req.birth_input.day,
            hour=req.birth_input.hour,
            minute=req.birth_input.minute,
            timezone_str=req.birth_input.timezone_str,
            latitude=req.birth_input.latitude,
            longitude=req.birth_input.longitude
        )

        master_evidence = CanonicalEvidencePipeline.generate_canonical_evidence(b_inp)
        query_dt = datetime.fromisoformat(req.query_datetime_iso) if req.query_datetime_iso else datetime.now(timezone.utc)

        snapshot = TransitEngine.calculate_transit_snapshot(
            natal_chart=master_evidence.canonical_chart,
            query_dt=query_dt
        )

        return snapshot.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/panchanga")
def get_panchanga(req: TransitRequest):
    try:
        query_dt = datetime.fromisoformat(req.query_datetime_iso) if req.query_datetime_iso else datetime.now(timezone.utc)
        panch = PanchangaEngine.calculate_panchanga(
            dt=query_dt,
            latitude=req.birth_input.latitude,
            longitude=req.birth_input.longitude,
            location_name=req.birth_input.place_name
        )
        return panch.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/muhurta")
def get_muhurta_suite(req: TransitRequest):
    try:
        query_dt = datetime.fromisoformat(req.query_datetime_iso) if req.query_datetime_iso else datetime.now(timezone.utc)
        muhurta = MuhurtaEngine.evaluate_all_activities(
            dt=query_dt,
            latitude=req.birth_input.latitude,
            longitude=req.birth_input.longitude,
            location_name=req.birth_input.place_name
        )
        return muhurta.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/jaimini")
def get_jaimini_suite(req: BirthProfileRequest):
    try:
        b_inp = BirthInput(
            name=req.name,
            year=req.year,
            month=req.month,
            day=req.day,
            hour=req.hour,
            minute=req.minute,
            timezone_str=req.timezone_str,
            latitude=req.latitude,
            longitude=req.longitude
        )

        master_evidence = CanonicalEvidencePipeline.generate_canonical_evidence(b_inp)
        return master_evidence.jaimini_suite.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/timing-windows")
def get_timing_suite(req: TransitRequest):
    try:
        b_inp = BirthInput(
            name=req.birth_input.name,
            year=req.birth_input.year,
            month=req.birth_input.month,
            day=req.birth_input.day,
            hour=req.birth_input.hour,
            minute=req.birth_input.minute,
            timezone_str=req.birth_input.timezone_str,
            latitude=req.birth_input.latitude,
            longitude=req.birth_input.longitude
        )

        master_evidence = CanonicalEvidencePipeline.generate_canonical_evidence(b_inp)
        return master_evidence.timing_suite.model_dump()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/interpret-evidence")
def interpret_evidence_ai(req: AIInterpretationRequest):
    try:
        # Section 29 Security: Server generates CanonicalAstrologyEvidence server-side from BirthInput.
        # Client CANNOT supply arbitrary evidence to AI.
        b_inp = BirthInput(
            name=req.birth_input.name,
            year=req.birth_input.year,
            month=req.birth_input.month,
            day=req.birth_input.day,
            hour=req.birth_input.hour,
            minute=req.birth_input.minute,
            timezone_str=req.birth_input.timezone_str,
            latitude=req.birth_input.latitude,
            longitude=req.birth_input.longitude
        )

        master_evidence = CanonicalEvidencePipeline.generate_canonical_evidence(b_inp)
        prediction_package = PredictionEngine.generate_all_predictions(master_evidence)

        # Select domain evidence server-side
        dom_code = req.domain.upper() if req.domain else "CAREER"
        dom_evidence = prediction_package.domain_predictions.get(
            dom_code,
            prediction_package.domain_predictions.get("CAREER")
        )

        ai_payload = {
            "master_evidence_hash": master_evidence.master_evidence_hash,
            "native_name": req.birth_input.name,
            "domain_evidence": dom_evidence.model_dump() if dom_evidence else {}
        }

        text = AIService.generate_interpretation(req.prompt, ai_payload)
        status = AIService.validate_interpretation(text, ai_payload)
        return {
            "domain": dom_code,
            "interpretation": text,
            "validation_status": status,
            "server_master_evidence_hash": master_evidence.master_evidence_hash
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
