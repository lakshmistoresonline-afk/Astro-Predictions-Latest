"""
Legacy Adapter Wrapper for Varga Engine.
Delegates completely to AuthoritativeVargaEngine (apps.api.engines.varga.engine).
Section 2 Compliance: Pure delegation wrapper over AuthoritativeVargaEngine! Zero compute_varga_sign_and_div imports!
"""
from typing import Dict, Any
from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.varga.models import Full16VargaSuite
from apps.api.engines.varga.engine import VargaEngine as AuthoritativeVargaEngine

class VargaEngine:
    """
    Adapter wrapper ensuring single source of truth delegation to AuthoritativeVargaEngine.
    """

    SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

    @classmethod
    def calculate_varga_suite(cls, canonical_chart: CanonicalVedicChart) -> Full16VargaSuite:
        """Delegates completely to AuthoritativeVargaEngine."""
        return AuthoritativeVargaEngine.calculate_all_16_vargas(canonical_chart)

    @classmethod
    def calculate_all_vargas(cls, canonical_chart: CanonicalVedicChart) -> dict:
        """
        Delegates completely to AuthoritativeVargaEngine and returns dictionary representation.
        """
        suite = AuthoritativeVargaEngine.calculate_all_16_vargas(canonical_chart)
        return suite.model_dump()
