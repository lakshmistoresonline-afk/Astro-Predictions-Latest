"""
Authoritative Vimshottari Dasha Engine Main Class for Astrovision.
Consumes Canonical Sidereal Moon State produced by Phase 2A.
Section 1..13 Compliance: Reconciles active_hierarchy and active_dasha_at_birth across all Dasha consumers.
"""
from datetime import datetime, timezone
from typing import Optional

from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.dasha.exceptions import InvalidMoonStateError, DashaCalculationError
from apps.api.engines.dasha.models import (
    BirthNakshatraInfo,
    BirthDashaBalance,
    FullVimshottariDashaResult,
    ActiveDashaHierarchy
)
from apps.api.engines.dasha.calculator import (
    calculate_birth_nakshatra_info,
    DASHA_YEARS,
    DAYS_PER_YEAR
)
from apps.api.engines.dasha.timeline import (
    generate_mahadasha_nodes,
    query_dasha_hierarchy_at
)
from apps.api.engines.dasha.hash import generate_dasha_calculation_hash

class AuthoritativeDashaEngine:
    """
    Authoritative Vimshottari Dasha Engine.
    Source Separation: Consumes Phase 2A Canonical Vedic Chart. Never calls Skyfield or recalculates Moon position.
    """

    @classmethod
    def calculate_dasha_suite(
        cls,
        canonical_chart: CanonicalVedicChart,
        query_datetime_utc: Optional[datetime] = None
    ) -> FullVimshottariDashaResult:
        """
        Calculates full Vimshottari Dasha suite from Phase 2A Canonical Vedic Chart.
        """
        if "Moon" not in canonical_chart.placements:
            raise InvalidMoonStateError("Canonical Vedic Chart is missing Moon placement.")

        moon_placement = canonical_chart.placements["Moon"]
        moon_sidereal_lon = moon_placement.sidereal_longitude

        # 1. Birth Nakshatra Info
        nak_info = calculate_birth_nakshatra_info(moon_sidereal_lon)

        # 2. Birth Datetime UTC
        birth_dt_utc = datetime.fromisoformat(canonical_chart.time_normalization.utc_datetime_iso)

        # 3. Birth Mahadasha Balance
        birth_md_lord = nak_info.nakshatra_lord
        total_md_years = DASHA_YEARS[birth_md_lord]
        rem_years = total_md_years * nak_info.remaining_fraction
        rem_days = rem_years * DAYS_PER_YEAR

        # 4. Generate 120-Year Mahadasha Sequence
        md_nodes = generate_mahadasha_nodes(birth_dt_utc, nak_info)
        first_md_end_iso = md_nodes[0].end_utc_iso

        birth_balance = BirthDashaBalance(
            mahadasha_lord=birth_md_lord,
            total_mahadasha_years=total_md_years,
            remaining_years=round(rem_years, 6),
            remaining_days=round(rem_days, 6),
            birth_utc_datetime_iso=birth_dt_utc.isoformat(),
            first_mahadasha_end_utc_iso=first_md_end_iso
        )

        # 5. Query Active Dasha Hierarchy at Birth (or target query datetime)
        target_query_dt = query_datetime_utc if query_datetime_utc else birth_dt_utc
        if target_query_dt.tzinfo is None:
            target_query_dt = target_query_dt.replace(tzinfo=timezone.utc)

        active_at_query = query_dasha_hierarchy_at(target_query_dt, md_nodes)

        # 6. Cryptographic Hash
        dasha_hash = generate_dasha_calculation_hash(
            birth_utc_iso=birth_dt_utc.isoformat(),
            moon_sidereal_lon=moon_sidereal_lon,
            astronomy_state_hash=canonical_chart.calculation_hash
        )

        return FullVimshottariDashaResult(
            birth_utc_datetime_iso=birth_dt_utc.isoformat(),
            moon_sidereal_longitude_deg=moon_sidereal_lon,
            nakshatra_info=nak_info,
            birth_balance=birth_balance,
            mahadashas=md_nodes,
            active_hierarchy=active_at_query,
            active_dasha_at_birth=active_at_query,
            dasha_convention="Parashari Vimshottari (120 Years)",
            time_convention="Tropical Solar Year (365.25 Days/Year)",
            calculation_hash=dasha_hash,
            astronomy_state_hash=canonical_chart.calculation_hash
        )

    @classmethod
    def get_dasha_at(
        cls,
        canonical_chart: CanonicalVedicChart,
        query_datetime_utc: datetime
    ) -> ActiveDashaHierarchy:
        """
        Queries active 5-level Dasha hierarchy for an arbitrary query datetime.
        """
        if query_datetime_utc.tzinfo is None:
            query_datetime_utc = query_datetime_utc.replace(tzinfo=timezone.utc)

        suite = cls.calculate_dasha_suite(canonical_chart, query_datetime_utc)
        return suite.active_hierarchy
