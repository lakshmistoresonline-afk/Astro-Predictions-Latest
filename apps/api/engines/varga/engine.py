"""
Authoritative 16-Varga Divisional Chart Engine for Astrovision.
Consumes Canonical Sidereal Longitudes produced by Phase 2A.
"""
import hashlib
import json
from typing import Dict, List, Optional

from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.varga.models import (
    VargaPlacement,
    VargaChart,
    Full16VargaSuite
)
from apps.api.engines.varga.rules import (
    VARGA_METADATA,
    compute_varga_sign_and_div
)

CLASSICAL_BODIES = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"
]

MODERN_BODIES = ["Uranus", "Neptune", "Pluto"]

ALL_SUPPORTED_DIVISIONS = [
    "D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12",
    "D16", "D20", "D24", "D27", "D30", "D40", "D45", "D60"
]

class VargaEngine:
    """
    16-Varga Divisional Chart Engine.
    Source Separation: Consumes Canonical Sidereal Chart. Never recalculates positions or calls Skyfield.
    """

    @classmethod
    def calculate_varga_chart(
        cls,
        canonical_chart: CanonicalVedicChart,
        division: str
    ) -> VargaChart:
        """Calculates a single Varga chart for a given division (e.g. 'D9')."""
        if division not in VARGA_METADATA:
            raise ValueError(f"Invalid or unsupported Varga division: '{division}'")

        meta = VARGA_METADATA[division]

        # 1. Process Ascendant
        asc_sid_lon = canonical_chart.ascendant.absolute_longitude
        asc_sign_idx, asc_sign_name, asc_div_idx, asc_deg = compute_varga_sign_and_div(division, asc_sid_lon)

        # Check Vargottama for Ascendant
        d1_asc_sign = canonical_chart.ascendant.sign
        d9_asc_sign_idx, d9_asc_sign_name, _, _ = compute_varga_sign_and_div("D9", asc_sid_lon)
        asc_vargottama = (d1_asc_sign == d9_asc_sign_name)

        asc_placement = VargaPlacement(
            body_name="Ascendant",
            d1_sidereal_longitude=asc_sid_lon,
            varga_sign=asc_sign_name,
            varga_sign_index=asc_sign_idx,
            varga_division_index=asc_div_idx,
            varga_degree_in_sign=asc_deg,
            is_vargottama=asc_vargottama
        )

        # 2. Process Planets
        placements: Dict[str, VargaPlacement] = {}
        for body_name, p in canonical_chart.placements.items():
            sid_lon = p.sidereal_longitude
            sign_idx, sign_name, div_idx, eff_deg = compute_varga_sign_and_div(division, sid_lon)

            # Check Vargottama (D1 sign == D9 sign)
            d1_sign = p.rashi.sign
            d9_sign_idx, d9_sign_name, _, _ = compute_varga_sign_and_div("D9", sid_lon)
            vargottama = (d1_sign == d9_sign_name)

            placements[body_name] = VargaPlacement(
                body_name=body_name,
                d1_sidereal_longitude=sid_lon,
                varga_sign=sign_name,
                varga_sign_index=sign_idx,
                varga_division_index=div_idx,
                varga_degree_in_sign=eff_deg,
                is_vargottama=vargottama
            )

        # 3. Calculation Hash
        payload = {
            "division": division,
            "chart_hash": canonical_chart.calculation_hash,
            "asc_sign": asc_sign_name,
            "sun_sign": placements.get("Sun", asc_placement).varga_sign,
            "moon_sign": placements.get("Moon", asc_placement).varga_sign
        }
        varga_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

        return VargaChart(
            division=division,
            division_number=meta["number"],
            division_name=meta["name"],
            ascendant=asc_placement,
            placements=placements,
            convention="Parashari Traditional Canonical Convention",
            source=meta["source"],
            calculation_hash=varga_hash
        )

    @classmethod
    def calculate_all_16_vargas(
        cls,
        canonical_chart: CanonicalVedicChart
    ) -> Full16VargaSuite:
        """Calculates all 16 Parashari Divisional Charts (D1 through D60)."""
        vargas: Dict[str, VargaChart] = {}
        vargottama_bodies: List[str] = []

        for div in ALL_SUPPORTED_DIVISIONS:
            vargas[div] = cls.calculate_varga_chart(canonical_chart, div)

        # Identify all Vargottama bodies from D9 Navamsa chart
        d9_chart = vargas["D9"]
        if d9_chart.ascendant.is_vargottama:
            vargottama_bodies.append("Ascendant")

        for body_name, pos in d9_chart.placements.items():
            if pos.is_vargottama:
                vargottama_bodies.append(body_name)

        return Full16VargaSuite(
            chart_hash=canonical_chart.calculation_hash,
            vargas=vargas,
            vargottama_bodies=vargottama_bodies
        )
