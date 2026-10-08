import logging
from datetime import datetime, timezone
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from apps.api.config import settings, validate_and_init_secrets
from apps.api.middleware.correlation import CorrelationIdMiddleware
from apps.api.engines.astronomy.provider import verify_de440s_kernel_status
from apps.api.engines.astronomy.exceptions import CalculationError, KernelNotFoundError
from apps.api.engines.vedic.exceptions import VedicEngineError, OutOfBoundaryError, TimezoneResolutionError
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.time_normalization import normalize_birth_time
from apps.api.engines.canonical_evidence import CanonicalEvidencePipeline, CanonicalAstrologyEvidence
from apps.api.engines.prediction_engine import PredictionEngine
from apps.api.engines.svg_chart_engine import SVGChartEngine
from apps.api.engines.report_engine import ReportGeneratorEngine
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
from apps.api.routers.geocoding import router as geocoding_router
from apps.api.db.database import init_db, get_database_status
from apps.api.exceptions import (
    AstrovisionException,
    AstrovisionValidationError,
    CalculationEngineError,
    AuthenticationError
)
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional

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
app.include_router(geocoding_router)

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
            "detail": "Internal server error.",
            "error_code": "INTERNAL_SERVER_ERROR",
            "request_id": req_id,
            "timestamp_iso": datetime.now(timezone.utc).isoformat()
        }
    )

@app.get("/health")
def health_check():
    de440s_valid, de440s_msg = verify_de440s_kernel_status()
    db_stat = get_database_status()
    ai_health = AIService.check_ai_provider_health()

    overall_healthy = de440s_valid and ("error" not in db_stat)

    return {
        "status": "healthy" if overall_healthy else "degraded",
        "api_status": "active",
        "database_status": db_stat,
        "ephemeris_status": "NASA JPL DE440s Verified" if de440s_valid else f"error: {de440s_msg}",
        "ai_provider": ai_health.get("ai_provider"),
        "ai_provider_status": ai_health.get("ai_provider_status"),
        "ai_generation_model_status": ai_health.get("generation_model_status"),
        "ai_validation_model_status": ai_health.get("validation_model_status"),
        "engine_version": "6.0.0-Celestial-Astrolabe"
    }

@app.get("/ready")
def readiness_check():
    de440s_valid, de440s_msg = verify_de440s_kernel_status()
    if not de440s_valid:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Ephemeris kernel not ready: {de440s_msg}"
        )
    return {"ready": True, "ephemeris_kernel": "NASA JPL DE440s"}

@app.get("/version")
def version_info():
    return {
        "app_name": settings.app_name,
        "version": "6.0.0",
        "calculation_mode": "Zero-Trust Live Calculation",
        "ephemeris_kernel": "de440s.bsp",
        "ayanamsha": "Lahiri (Chitra Paksha)"
    }

class BirthProfileRequest(BaseModel):
    name: str = Field(min_length=1, description="Native's full name")
    year: int = Field(ge=1850, le=2150)
    month: int = Field(ge=1, le=12)
    day: int = Field(ge=1, le=31)
    hour: int = Field(ge=0, le=23)
    minute: int = Field(ge=0, le=59)
    second: Optional[int] = Field(default=0, ge=0, le=59)
    timezone_str: str = Field(description="Authoritative IANA timezone e.g. 'Asia/Kolkata'")
    latitude: float = Field(ge=-90.0, le=90.0)
    longitude: float = Field(ge=-180.0, le=180.0)
    place_name: str = Field(default="Unknown Place")
    country: str = Field(default="Unknown Country")
    zodiac_system: Optional[str] = Field(default="sidereal")
    ayanamsha: Optional[str] = Field(default="lahiri")

class AIInterpretationApiRequest(BaseModel):
    birth_input: Dict[str, Any]
    prompt: Optional[str] = "Explain domain factors"
    domain: Optional[str] = "CAREER"

class TransitRequest(BaseModel):
    birth_input: BirthProfileRequest
    query_datetime_utc: Optional[str] = None

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
    except (ValueError, TypeError, VedicEngineError, CalculationError) as e:
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
            second=req.birth_input.second if req.birth_input.second is not None else 0,
            timezone_str=req.birth_input.timezone_str,
            latitude=req.birth_input.latitude,
            longitude=req.birth_input.longitude
        )
        master_ev = CanonicalEvidencePipeline.generate_canonical_evidence(b_inp)
        q_dt = None
        if req.query_datetime_utc:
            q_dt = datetime.fromisoformat(req.query_datetime_utc)
            if q_dt.tzinfo is None:
                q_dt = q_dt.replace(tzinfo=timezone.utc)

        snapshot = TransitEngine.calculate_transit_snapshot(master_ev.canonical_chart, query_dt=q_dt)
        return snapshot.model_dump()
    except (ValueError, TypeError, VedicEngineError, CalculationError) as e:
        raise AstrovisionValidationError(str(e))
    except AstrovisionException:
        raise
    except Exception as e:
        logger.exception("Error in get_transit_snapshot")
        raise CalculationEngineError("Transit calculation failed.")

@app.post("/api/v1/panchanga")
def calculate_panchanga(req: TransitRequest):
    try:
        b_inp = BirthInput(
            name=req.birth_input.name,
            year=req.birth_input.year,
            month=req.birth_input.month,
            day=req.birth_input.day,
            hour=req.birth_input.hour,
            minute=req.birth_input.minute,
            second=req.birth_input.second if req.birth_input.second is not None else 0,
            timezone_str=req.birth_input.timezone_str,
            latitude=req.birth_input.latitude,
            longitude=req.birth_input.longitude
        )
        if req.query_datetime_utc:
            q_dt = datetime.fromisoformat(req.query_datetime_utc)
            if q_dt.tzinfo is None:
                q_dt = q_dt.replace(tzinfo=timezone.utc)
        else:
            time_norm = normalize_birth_time(b_inp)
            q_dt = datetime.fromisoformat(time_norm.utc_datetime_iso)

        res = PanchangaEngine.calculate_panchanga(
            dt=q_dt,
            latitude=b_inp.latitude,
            longitude=b_inp.longitude,
            elevation=b_inp.elevation_m,
            location_name=b_inp.name,
            timezone_str=b_inp.timezone_str
        )
        return res.model_dump()
    except (ValueError, TypeError, VedicEngineError, CalculationError) as e:
        raise AstrovisionValidationError(str(e))
    except AstrovisionException:
        raise
    except Exception as e:
        logger.exception("Error in calculate_panchanga")
        raise CalculationEngineError("Panchanga calculation failed.")

@app.post("/api/v1/muhurta")
def calculate_muhurta_suite(req: TransitRequest):
    try:
        b_inp = BirthInput(
            name=req.birth_input.name,
            year=req.birth_input.year,
            month=req.birth_input.month,
            day=req.birth_input.day,
            hour=req.birth_input.hour,
            minute=req.birth_input.minute,
            second=req.birth_input.second if req.birth_input.second is not None else 0,
            timezone_str=req.birth_input.timezone_str,
            latitude=req.birth_input.latitude,
            longitude=req.birth_input.longitude
        )
        if req.query_datetime_utc:
            q_dt = datetime.fromisoformat(req.query_datetime_utc)
            if q_dt.tzinfo is None:
                q_dt = q_dt.replace(tzinfo=timezone.utc)
        else:
            time_norm = normalize_birth_time(b_inp)
            q_dt = datetime.fromisoformat(time_norm.utc_datetime_iso)

        panchanga = PanchangaEngine.calculate_panchanga(
            dt=q_dt,
            latitude=b_inp.latitude,
            longitude=b_inp.longitude,
            elevation=b_inp.elevation_m,
            location_name=b_inp.name,
            timezone_str=b_inp.timezone_str
        )

        res = MuhurtaEngine.calculate_muhurta_suite(panchanga)
        return res.model_dump()
    except (ValueError, TypeError, VedicEngineError, CalculationError) as e:
        raise AstrovisionValidationError(str(e))
    except AstrovisionException:
        raise
    except Exception as e:
        logger.exception("Error in calculate_muhurta_suite")
        raise CalculationEngineError("Muhurta evaluation failed.")

@app.post("/api/v1/jaimini")
def calculate_jaimini_suite(req: BirthProfileRequest):
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
        master_ev = CanonicalEvidencePipeline.generate_canonical_evidence(b_inp)
        res = JaiminiEngine.calculate_jaimini_suite(master_ev.canonical_chart)
        return res.model_dump()
    except (ValueError, TypeError, VedicEngineError, CalculationError) as e:
        raise AstrovisionValidationError(str(e))
    except AstrovisionException:
        raise
    except Exception as e:
        logger.exception("Error in calculate_jaimini_suite")
        raise CalculationEngineError("Jaimini calculation failed.")

@app.post("/api/v1/timing-windows")
def calculate_predictive_timing(req: TransitRequest):
    try:
        b_inp = BirthInput(
            name=req.birth_input.name,
            year=req.birth_input.year,
            month=req.birth_input.month,
            day=req.birth_input.day,
            hour=req.birth_input.hour,
            minute=req.birth_input.minute,
            second=req.birth_input.second if req.birth_input.second is not None else 0,
            timezone_str=req.birth_input.timezone_str,
            latitude=req.birth_input.latitude,
            longitude=req.birth_input.longitude
        )
        master_ev = CanonicalEvidencePipeline.generate_canonical_evidence(b_inp)
        q_dt = None
        if req.query_datetime_utc:
            q_dt = datetime.fromisoformat(req.query_datetime_utc)
            if q_dt.tzinfo is None:
                q_dt = q_dt.replace(tzinfo=timezone.utc)

        res = TimingEngine.generate_timing_suite(master_ev.canonical_chart, query_dt=q_dt)
        return res.model_dump()
    except (ValueError, TypeError, VedicEngineError, CalculationError) as e:
        raise AstrovisionValidationError(str(e))
    except AstrovisionException:
        raise
    except Exception as e:
        logger.exception("Error in calculate_predictive_timing")
        raise CalculationEngineError("Predictive timing evaluation failed.")

@app.post("/api/v1/interpret-evidence")
def interpret_evidence_ai(req: AIInterpretationApiRequest):
    try:
        bi_dict = req.birth_input
        b_inp = BirthInput(
            name=str(bi_dict.get("name", "Native")),
            year=int(bi_dict["year"]),
            month=int(bi_dict["month"]),
            day=int(bi_dict["day"]),
            hour=int(bi_dict["hour"]),
            minute=int(bi_dict["minute"]),
            second=int(bi_dict.get("second", 0)),
            timezone_str=str(bi_dict["timezone_str"]).strip(),
            latitude=float(bi_dict["latitude"]),
            longitude=float(bi_dict["longitude"])
        )

        master_evidence = CanonicalEvidencePipeline.generate_canonical_evidence(b_inp)
        domain = req.domain or "CAREER"
        prompt = req.prompt or "Explain domain factors"

        interpretation_res = AIService.synthesize_interpretation(
            prompt=prompt,
            evidence=master_evidence.model_dump(),
            domain=domain
        )

        return interpretation_res
    except (ValueError, TypeError, VedicEngineError, CalculationError) as e:
        raise AstrovisionValidationError(str(e))
    except AstrovisionException:
        raise
    except Exception as e:
        logger.exception("Error in interpret_evidence_ai")
        raise CalculationEngineError("AI interpretation synthesis failed.")
