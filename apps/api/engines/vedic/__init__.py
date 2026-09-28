"""
Canonical Vedic Engine Package for Astrovision (Phase 2A).
"""
from apps.api.engines.vedic.exceptions import (
    VedicEngineError,
    InvalidBirthDataError,
    TimezoneResolutionError,
    OutOfBoundaryError,
    AstronomyExecutionError
)
from apps.api.engines.vedic.models import (
    BirthInput,
    TimeNormalization,
    RashiPosition,
    NakshatraPada,
    PlanetaryVedicPlacement,
    WholeSignHouse,
    CanonicalVedicChart
)
from apps.api.engines.vedic.time_normalization import normalize_birth_time
from apps.api.engines.vedic.rashi import calculate_rashi
from apps.api.engines.vedic.nakshatra import calculate_nakshatra_pada
from apps.api.engines.vedic.houses import generate_whole_sign_houses
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart

__all__ = [
    "VedicEngineError",
    "InvalidBirthDataError",
    "TimezoneResolutionError",
    "OutOfBoundaryError",
    "AstronomyExecutionError",
    "BirthInput",
    "TimeNormalization",
    "RashiPosition",
    "NakshatraPada",
    "PlanetaryVedicPlacement",
    "WholeSignHouse",
    "CanonicalVedicChart",
    "normalize_birth_time",
    "calculate_rashi",
    "calculate_nakshatra_pada",
    "generate_whole_sign_houses",
    "build_canonical_vedic_chart"
]
