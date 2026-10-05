"""
Legacy Adapter Wrapper for Strength Engine (Shadbala & Ashtakavarga).
Delegates directly to Authoritative ShadbalaEngine and AshtakavargaEngine.
Section 1 Compliance: Pure delegation adapter invoking AuthoritativeShadbalaEngine and AuthoritativeAshtakavargaEngine!
"""
from typing import Dict, Any
from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.varga.models import Full16VargaSuite
from apps.api.engines.strength.shadbala import ShadbalaEngine as AuthoritativeShadbalaEngine
from apps.api.engines.strength.ashtakavarga import AshtakavargaEngine as AuthoritativeAshtakavargaEngine
from apps.api.engines.strength.models import ShadbalaSuiteResult, AshtakavargaSuiteResult

class StrengthEngine:
    """
    Adapter wrapper ensuring single source of truth delegation to canonical engines.
    """

    @classmethod
    def calculate_shadbala_suite(
        cls,
        canonical_chart: CanonicalVedicChart,
        varga_suite: Full16VargaSuite
    ) -> ShadbalaSuiteResult:
        """Delegates completely to AuthoritativeShadbalaEngine."""
        return AuthoritativeShadbalaEngine.calculate_shadbala_suite(canonical_chart, varga_suite)

    @classmethod
    def calculate_ashtakavarga(
        cls,
        canonical_chart: CanonicalVedicChart
    ) -> AshtakavargaSuiteResult:
        """Delegates completely to AuthoritativeAshtakavargaEngine."""
        return AuthoritativeAshtakavargaEngine.calculate_ashtakavarga(canonical_chart)
