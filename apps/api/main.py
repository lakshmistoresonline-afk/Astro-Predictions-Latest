"""
Master FastAPI Application Entry Point for Astrovision (Phase 2E-R4.1-R12-R10).
Exposes deterministic local astrology APIs backed by NASA JPL DE440s, 16 Vargas, 5-Level Dasha,
Shadbala, Ashtakavarga, Transits, Panchanga, Muhurta, Jaimini, Timing Engine, and Server-Owned Evidence AI Handoff.
Section 1..13 Compliance:
- Correlation ID middleware (X-Request-ID).
- Structured JSON error responses across all failure classes.
- Full server-side diagnostic logging with zero client information leakage.
"""
import os
import hashlib
import logging
import zoneinfo
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

from apps.api.config import settings
from apps.api.exceptions import (
    AstrovisionException,
    AstrovisionValidationError,
    TimezoneError,
    ResourceNotFoundError,
    AuthenticationError,
    AuthorizationError,
    AstronomyKernelError,
    CalculationEngineError
)
from apps.api.middleware.correlation import CorrelationIdMiddleware
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
from apps.api.routers.persistence import router as persistence_router
from apps.api.routers.auth import router as auth_router
from apps.api.db.database import init_db, get_database_status

logger = logging.getLogger("astrovision.api")

app = FastAPI(
    title=settings.app_name,
    version="6.0.0",
    description="Deterministic Astrology Computation, Transit, Panchanga, Muhurta, Jaimini and Prediction Platform"
)

app.add_middleware(CorrelationIdMiddleware)

# Environment-configured CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_export_router)
app.include_router(persistence_router)

from apps.api.config import settings, validate_and_init_secrets

@app.on_event("startup")
def on_startup():
    validate_and_init_secrets()
    init_db()

# Structured Error Response Exception Handlers
@app.exception_handler(AstrovisionException)
async def astrovision_exception_handler(request: Request, exc: AstrovisionException):
    req_id = getattr(request.state, "request_id", "req_unknown")
    logger.warning(f"[{req_id}] Domain exception: {exc.message} ({exc.error_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "error_code": exc.error_code,
            "request_id": req_id,
            "timestamp_iso": datetime.now(timezone.utc).isoformat()
        }
    )

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    req_id = getattr(request.state, "request_id", "req_unknown")
    logger.warning(f"[{req_id}] HTTP exception {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": str(exc.detail),
            "error_code": f"HTTP_ERROR_{exc.status_code}",
            "request_id": req_id,
            "timestamp_iso": datetime.now(timezone.utc).isoformat()
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    req_id = getattr(request.state, "request_id", "req_unknown")
    logger.warning(f"[{req_id}] Request validation error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid request payload or parameters.",
            "error_code": "VALIDATION_ERROR",
            "request_id": req_id,
            "timestamp_iso": datetime.now(timezone.utc).isoformat()
        }
    )

@app.exception_handler(Exception)
async def uncaught_exception_handler(request: Request, exc: Exception):
    req_id = getattr(request.state, "request_id", "req_unknown")
    logger.exception(f"[{req_id}] Uncaught internal server error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred while processing the request.",
            "error_code": "INTERNAL_SERVER_ERROR",
            "request_id": req_id,
            "timestamp_iso": datetime.now(timezone.utc).isoformat()
        }
    )

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
    name: str = Field(description="Full birth name")
    year: int = Field(description="Four-digit Gregorian birth year (1850-2150)")
    month: int = Field(description="Birth month (1-12)")
    day: int = Field(description="Birth day (1-31)")
    hour: int = Field(description="Local civil hour (0-23)")
    minute: int = Field(description="Local civil minute (0-59)")
    second: Optional[int] = Field(default=0, description="Local civil second (0-59)")
    timezone_str: str = Field(description="Authoritative IANA timezone string e.g. 'Asia/Kolkata'")
    latitude: float = Field(description="Geographic latitude in degrees [-90.0, 90.0]")
    longitude: float = Field(description="Geographic longitude in degrees [-180.0, 180.0]")
    place_name: str = Field(description="City or place name")
    country: str = Field(description="Country name")
    zodiac_system: Optional[str] = Field(default="sidereal", description="Zodiac system: 'sidereal' (Vedic Lahiri) or 'tropical' (Western)")
    ayanamsha: Optional[str] = Field(default="lahiri", description="Ayanamsha mode: 'lahiri' (Chitra Paksha)")
    birth_time_accuracy: Optional[str] = Field(default="exact", description="Birth time accuracy level")

class TransitRequest(BaseModel):
    birth_input: BirthProfileRequest
    query_datetime_iso: Optional[str] = Field(default=None, description="ISO query datetime string, or None for current observer time")

class AIInterpretationRequest(BaseModel):
    birth_input: BirthProfileRequest
    prompt: str = Field(description="Interpretation topic request prompt")
    domain: Optional[str] = Field(default="CAREER", description="Prediction domain code")

@app.get("/health")
def health_check():
    de440s_valid, de440s_msg = verify_de440s_kernel_status()
    db_stat = get_database_status()
    return {
        "status": "healthy" if (de440s_valid and "error" not in db_stat) else "degraded",
        "api_status": "active",
        "database_status": db_stat,
        "ephemeris_status": "NASA JPL DE440s Verified" if de440s_valid else f"error: {de440s_msg}",
        "ai_model_generation": settings.ai_model_generation,
        "ai_model_validation": settings.ai_model_validation,
        "engine_version": "6.0.0-Celestial-Astrolabe"
    }

@app.get("/ready")
def readiness_check():
    de440s_valid, de440s_msg = verify_de440s_kernel_status()
    if not de440s_valid:
        raise AstronomyKernelError(f"Ephemeris kernel DE440s unavailable: {de440s_msg}")
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
    except (ValueError, TypeError) as e:
        raise AstrovisionValidationError(str(e))
    except AstrovisionException:
        raise
    except Exception as e:
        logger.exception("Error in calculate_birth_profile")
        raise CalculationEngineError("Calculation failed due to internal engine error.")

@app.post("/api/v1/transits")
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
        tz_name = req.birth_input.timezone_str
        tz = zoneinfo.ZoneInfo(tz_name)
        if req.query_datetime_iso:
            dt_parsed = datetime.fromisoformat(req.query_datetime_iso)
            query_dt = dt_parsed if dt_parsed.tzinfo else dt_parsed.replace(tzinfo=tz)
        else:
            query_dt = datetime.now(tz)

        snapshot = TransitEngine.calculate_transit_snapshot(
            natal_chart=master_evidence.canonical_chart,
            query_dt=query_dt
        )

        return snapshot.model_dump()
    except (ValueError, TypeError) as e:
        raise AstrovisionValidationError(str(e))
    except AstrovisionException:
        raise
    except Exception as e:
        logger.exception("Error in get_transit_snapshot")
        raise CalculationEngineError("Transit calculation failed due to internal engine error.")

@app.post("/api/v1/panchanga")
def get_panchanga(req: TransitRequest):
    try:
        tz_name = req.birth_input.timezone_str
        tz = zoneinfo.ZoneInfo(tz_name)
        if req.query_datetime_iso:
            dt_parsed = datetime.fromisoformat(req.query_datetime_iso)
            query_dt = dt_parsed if dt_parsed.tzinfo else dt_parsed.replace(tzinfo=tz)
        else:
            query_dt = datetime.now(tz)

        panch = PanchangaEngine.calculate_panchanga(
            dt=query_dt,
            latitude=req.birth_input.latitude,
            longitude=req.birth_input.longitude,
            location_name=req.birth_input.place_name,
            timezone_str=tz_name
        )
        return panch.model_dump()
    except (ValueError, TypeError) as e:
        raise AstrovisionValidationError(str(e))
    except AstrovisionException:
        raise
    except Exception as e:
        logger.exception("Error in get_panchanga")
        raise CalculationEngineError("Panchanga calculation failed due to internal engine error.")

@app.post("/api/v1/muhurta")
def get_muhurta_suite(req: TransitRequest):
    try:
        tz_name = req.birth_input.timezone_str
        tz = zoneinfo.ZoneInfo(tz_name)
        if req.query_datetime_iso:
            dt_parsed = datetime.fromisoformat(req.query_datetime_iso)
            query_dt = dt_parsed if dt_parsed.tzinfo else dt_parsed.replace(tzinfo=tz)
        else:
            query_dt = datetime.now(tz)

        muhurta = MuhurtaEngine.evaluate_all_activities(
            dt=query_dt,
            latitude=req.birth_input.latitude,
            longitude=req.birth_input.longitude,
            location_name=req.birth_input.place_name
        )
        return muhurta.model_dump()
    except (ValueError, TypeError) as e:
        raise AstrovisionValidationError(str(e))
    except AstrovisionException:
        raise
    except Exception as e:
        logger.exception("Error in get_muhurta_suite")
        raise CalculationEngineError("Muhurta calculation failed due to internal engine error.")

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
    except (ValueError, TypeError) as e:
        raise AstrovisionValidationError(str(e))
    except AstrovisionException:
        raise
    except Exception as e:
        logger.exception("Error in get_jaimini_suite")
        raise CalculationEngineError("Jaimini calculation failed due to internal engine error.")

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
    except (ValueError, TypeError) as e:
        raise AstrovisionValidationError(str(e))
    except AstrovisionException:
        raise
    except Exception as e:
        logger.exception("Error in get_timing_suite")
        raise CalculationEngineError("Timing window calculation failed due to internal engine error.")

@app.post("/api/v1/interpret-evidence")
def interpret_evidence_ai(req: AIInterpretationRequest):
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
        prediction_package = PredictionEngine.generate_all_predictions(master_evidence)

        dom_code = req.domain.upper() if req.domain else "CAREER"
        if dom_code not in prediction_package.domain_predictions:
            raise AstrovisionValidationError(f"Unsupported domain '{req.domain}'. Supported domains: {list(prediction_package.domain_predictions.keys())}")

        dom_evidence = prediction_package.domain_predictions[dom_code]

        ai_payload = {
            "master_evidence_hash": master_evidence.master_evidence_hash,
            "native_name": req.birth_input.name,
            "domain_evidence": dom_evidence.model_dump() if dom_evidence else {}
        }

        ai_result = AIService.synthesize_interpretation(req.prompt, ai_payload, domain=dom_code)
        return ai_result
    except AstrovisionException:
        raise
    except (ValueError, TypeError) as e:
        raise AstrovisionValidationError(str(e))
    except Exception as e:
        logger.exception("Error in interpret_evidence_ai")
        raise CalculationEngineError("AI interpretation synthesis failed due to internal service error.")
