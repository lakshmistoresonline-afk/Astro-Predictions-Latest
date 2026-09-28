"""
Authoritative 16-Varga Divisional Chart Engine Package for Astrovision (Phase 2B).
"""
from apps.api.engines.varga.models import (
    VargaPlacement,
    VargaChart,
    Full16VargaSuite
)
from apps.api.engines.varga.rules import (
    VARGA_METADATA,
    compute_varga_sign_and_div
)
from apps.api.engines.varga.engine import (
    VargaEngine,
    CLASSICAL_BODIES,
    MODERN_BODIES,
    ALL_SUPPORTED_DIVISIONS
)

__all__ = [
    "VargaPlacement",
    "VargaChart",
    "Full16VargaSuite",
    "VARGA_METADATA",
    "compute_varga_sign_and_div",
    "VargaEngine",
    "CLASSICAL_BODIES",
    "MODERN_BODIES",
    "ALL_SUPPORTED_DIVISIONS"
]
