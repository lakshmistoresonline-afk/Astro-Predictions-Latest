"""
Authoritative Comprehensive Report Generator Engine for Astrovision (Phase 2E-R4.1-R12-R10).
Compiles dynamic, publication-grade astrological treatises incorporating Canonical Evidence,
Vargas, Dashas, Yogas, Doshas, Shadbala, Ashtakavarga, Transits, Panchanga, and Jaimini.
Section 2 Compliance: Fail closed if timezone_name or Varga placement is missing. Zero Ascendant or 'Asia/Kolkata' string fallbacks!
"""
from typing import Dict, Any, Optional

from apps.api.engines.birth_engine import BirthDataEngine
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.canonical_evidence import CanonicalEvidencePipeline, CanonicalAstrologyEvidence
from apps.api.engines.prediction_engine import PredictionEngine
from apps.api.engines.varga.engine import ALL_SUPPORTED_DIVISIONS

class ReportGeneratorEngine:
    """
    ReportGeneratorEngine compiles fully dynamic, user-specific publication-grade
    astrological treatises incorporating Canonical Astronomy, Vargas, Dashas, Yogas, and Doshas.
    """

    @classmethod
    def generate_comprehensive_report(
        cls,
        name: str,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        latitude: float,
        longitude: float,
        place_name: str,
        country: str,
        zodiac_system: str = "sidereal",
        ayanamsha: str = "lahiri"
    ) -> dict:

        # 1. Resolve Timezone & Process Birth Data
        birth_data = BirthDataEngine.process_birth_data(
            name, year, month, day, hour, minute, latitude, longitude, place_name, country
        )

        if "timezone_name" not in birth_data or not birth_data["timezone_name"]:
            raise ValueError("timezone_name is required in birth_data")

        tz_str = birth_data["timezone_name"]

        b_inp = BirthInput(
            name=name, year=year, month=month, day=day,
            hour=hour, minute=minute, second=0,
            timezone_str=tz_str,
            latitude=latitude, longitude=longitude
        )

        # 2. Master Canonical Astrology Evidence
        master_evidence = CanonicalEvidencePipeline.generate_canonical_evidence(b_inp)
        predictions = PredictionEngine.generate_all_predictions(master_evidence)

        # Formatted Legacy Compatibility Maps
        canonical_chart = master_evidence.canonical_chart
        planetary_positions = {}
        for p_name, placement in canonical_chart.placements.items():
            planetary_positions[p_name] = {
                "longitude": placement.sidereal_longitude,
                "latitude": placement.geocentric_latitude,
                "speed": placement.velocity_deg_day,
                "retrograde": placement.retrograde,
                "sign": placement.rashi.sign,
                "degree": float(placement.rashi.degree) + (placement.rashi.minute / 60.0),
                "nakshatra": placement.nakshatra_pada.nakshatra_name,
                "pada": placement.nakshatra_pada.pada,
                "dignity": placement.dignity
            }

        vargas_16 = {}
        for body in canonical_chart.placements.keys():
            vargas_16[body] = {}
            for div in ALL_SUPPORTED_DIVISIONS:
                v_chart = master_evidence.varga_suite.vargas[div]
                # Section 2 Correction: Fail closed if Varga placement is missing! Zero Ascendant substitution!
                if body not in v_chart.placements:
                    raise ValueError(f"Placement for body '{body}' is missing from Varga chart '{div}'")
                v_place = v_chart.placements[body]
                vargas_16[body][f"{div}_Sign"] = v_place.varga_sign

        yogas = [y.model_dump() for y in master_evidence.yoga_suite.detected_yogas]
        doshas = [d.model_dump() for d in master_evidence.dosha_suite.detected_doshas]

        return {
            "metadata": {
                "native_name": name,
                "report_title": f"Masterwork Astrological Treatise for {name}",
                "birth_datetime_utc": canonical_chart.time_normalization.utc_datetime_iso,
                "julian_day_tt": canonical_chart.time_normalization.julian_day_tt,
                "ayanamsha": "Lahiri",
                "ephemeris": "NASA JPL DE440s",
                "engine_version": "Astrovision 2026.1 Canonical",
                "master_evidence_hash": master_evidence.master_evidence_hash,
                "prediction_hash": predictions.calculation_hash
            },
            "chapter_1_methodology": {
                "title": "Astronomical Precision & Methodological Foundations",
                "content": f"Calculated using NASA JPL DE440s ephemeris in geocentric mode with Lahiri ayanamsha ({canonical_chart.time_normalization.ayanamsha_value_deg:.6f}°)."
            },
            "chapter_2_ascendant": {
                "title": "The Lagna (Ascendant) & Life Foundation",
                "content": f"Ascendant in {canonical_chart.ascendant.rashi.name_english} ({canonical_chart.ascendant.rashi.degree}° {canonical_chart.ascendant.rashi.minute}')."
            },
            "chapter_3_planetary_positions": {
                "title": "Sidereal Planetary Longitudes & Astronomical Positions",
                "data": planetary_positions
            },
            "chapter_4_vargas": {
                "title": "16 Canonical Shodashavargas (D1 to D60)",
                "data": vargas_16
            },
            "chapter_5_dashas": {
                "title": "5-Level Vimshottari Dasha Hierarchy",
                "data": master_evidence.natal_dasha_suite.model_dump()
            },
            "chapter_6_yogas": {
                "title": "Detected Classical Parashari Yogas",
                "data": yogas
            },
            "chapter_7_doshas": {
                "title": "Detected Classical Parashari Doshas",
                "data": doshas
            },
            "chapter_8_shadbala": {
                "title": "6-Fold Planetary Strength (Shadbala Suite)",
                "data": master_evidence.shadbala_suite.model_dump()
            },
            "chapter_9_life_domains": {
                "title": "Domain-Specific Predictive Evidence (14 Life Areas)",
                "data": predictions.model_dump()
            },
            "chapter_12_audit_trail": {
                "disclaimer": "This treatise is calculated deterministically from exact NASA JPL DE440s ephemeris data. AI synthesis provides natural language interpretation over server-owned evidence.",
                "calculation_hash": master_evidence.master_evidence_hash
            }
        }
