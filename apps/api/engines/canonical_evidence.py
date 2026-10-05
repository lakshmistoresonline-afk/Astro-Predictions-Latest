"""
Canonical Astrology Evidence Master Schema and Orchestration Pipeline.
Section 1, 2, 3, 4, 5, 6 Compliance:
- Complete semantic separation between Natal Evidence (immutable) and Temporal Evidence (query-date dependent).
- Natal calculation hash is 100% STABLE across any query_dt.
- Zero hidden current-time (`datetime.now()`) defaults inside canonical pipeline!
- Zero planet fallbacks (`else "Sun"` removed)!
"""
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from apps.api.engines.vedic.models import BirthInput, CanonicalVedicChart
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.astronomy.provider import BaseAstronomyProvider
from apps.api.engines.astronomy.providers.skyfield_jpl import SkyfieldJPLProvider
from apps.api.engines.varga.engine import VargaEngine
from apps.api.engines.varga.models import Full16VargaSuite
from apps.api.engines.varga.evidence_adapter import VargaEvidenceAdapter, VargaSuiteEvidence
from apps.api.engines.dasha.engine import DashaEngine
from apps.api.engines.dasha.models import DashaSuiteResult, ActiveDashaHierarchy
from apps.api.engines.yogas.evaluator import YogaEvaluator
from apps.api.engines.yogas.models import YogaSuiteResult
from apps.api.engines.doshas.evaluator import DoshaEvaluator
from apps.api.engines.doshas.models import DoshaSuiteResult
from apps.api.engines.strength.shadbala import ShadbalaEngine
from apps.api.engines.strength.models import ShadbalaSuiteResult
from apps.api.engines.strength.shadbala_adapter import ShadbalaEvidenceAdapter, ShadbalaEvidencePackage
from apps.api.engines.strength.ashtakavarga import AshtakavargaEngine
from apps.api.engines.strength.models import AshtakavargaSuiteResult
from apps.api.engines.strength.ashtakavarga_adapter import AshtakavargaEvidenceAdapter, AshtakavargaPredictiveEvidence
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

class CanonicalAstrologyEvidence(BaseModel):
    """
    Master Output Contract unifying all deterministic local astrology calculations.
    Every downstream prediction, AI prompt, report, and frontend component consumes this object.
    """
    birth_input: BirthInput
    canonical_chart: CanonicalVedicChart
    varga_suite: Full16VargaSuite
    varga_evidence: VargaSuiteEvidence
    natal_dasha_suite: DashaSuiteResult = Field(description="Pure natal Dasha timeline & birth balance calculated at birth UTC")
    active_dasha_hierarchy: Optional[ActiveDashaHierarchy] = Field(default=None, description="Active Dasha lords evaluated at query_dt")
    yoga_suite: YogaSuiteResult
    dosha_suite: DoshaSuiteResult
    shadbala_suite: ShadbalaSuiteResult
    shadbala_evidence: ShadbalaEvidencePackage
    ashtakavarga_suite: AshtakavargaSuiteResult
    ashtakavarga_evidence: AshtakavargaPredictiveEvidence
    jaimini_suite: JaiminiSuiteResult
    transit_snapshot: Optional[TransitSnapshot] = Field(default=None, description="Temporal transit snapshot if query_dt provided")
    panchanga: Optional[PanchangaResult] = Field(default=None, description="Temporal Panchanga if query_dt provided")
    muhurta_suite: Optional[MuhurtaSuiteResult] = Field(default=None, description="Temporal Muhurta evaluation if query_dt provided")
    timing_suite: Optional[TimingSuiteResult] = Field(default=None, description="Temporal timing windows if query_dt provided")
    natal_calculation_hash: str = Field(description="100% immutable calculation hash for pure birth chart facts")
    temporal_calculation_hash: Optional[str] = Field(default=None, description="Hash for query_dt temporal evidence")
    master_evidence_hash: str

class CanonicalEvidencePipeline:
    """
    Authoritative Master Pipeline.
    Executes the complete local deterministic astrology calculation chain once.
    """

    @classmethod
    def generate_canonical_evidence(
        cls,
        birth_input: BirthInput,
        query_dt: Optional[datetime] = None,
        astronomy_provider: Optional[BaseAstronomyProvider] = None
    ) -> CanonicalAstrologyEvidence:
        if not astronomy_provider:
            astronomy_provider = SkyfieldJPLProvider()

        # 1. Canonical Vedic Chart (D1, Nakshatra, Houses, Astronomical State)
        canonical_chart = build_canonical_vedic_chart(birth_input, astronomy_provider)

        # 2. 16 Vargas & Varga Evidence
        varga_suite = VargaEngine.calculate_all_16_vargas(canonical_chart)
        varga_evidence = VargaEvidenceAdapter.extract_evidence_suite(varga_suite)

        # 3. Pure Natal Dasha Suite (Evaluated strictly at birth UTC datetime for 100% natal stability)
        birth_utc_dt = datetime.fromisoformat(canonical_chart.time_normalization.utc_datetime_iso)
        natal_dasha_suite = DashaEngine.calculate_dasha_suite(canonical_chart, birth_utc_dt)

        # 4. Yogas & Doshas
        yoga_suite = YogaEvaluator.evaluate_all_yogas(canonical_chart)
        dosha_suite = DoshaEvaluator.evaluate_all_doshas(canonical_chart)

        # 5. Shadbala & Evidence Package
        shadbala_suite = ShadbalaEngine.calculate_shadbala_suite(canonical_chart, varga_suite)
        shadbala_evidence = ShadbalaEvidenceAdapter.extract_evidence(shadbala_suite)

        # 6. Ashtakavarga (BAV & SAV) & Predictive Evidence
        ashtakavarga_suite = AshtakavargaEngine.calculate_ashtakavarga(canonical_chart)
        ashtakavarga_evidence = AshtakavargaEvidenceAdapter.extract_evidence(ashtakavarga_suite)

        # 7. Jaimini Engine
        jaimini_suite = JaiminiEngine.calculate_jaimini_suite(canonical_chart)

        # Pure Natal Calculation Hash (Guaranteed STABLE across query dates)
        natal_payload = {
            "chart_hash": canonical_chart.calculation_hash,
            "varga_hash": varga_suite.calculation_hash,
            "natal_dasha_hash": natal_dasha_suite.calculation_hash,
            "yoga_hash": yoga_suite.rule_set_version,
            "shadbala_hash": shadbala_suite.calculation_hash,
            "ashtakavarga_hash": ashtakavarga_suite.calculation_hash,
            "jaimini_hash": jaimini_suite.calculation_hash
        }
        natal_hash = hashlib.sha256(json.dumps(natal_payload, sort_keys=True).encode("utf-8")).hexdigest()

        # 8. Optional Temporal Calculations (Executed ONLY if query_dt is explicitly provided)
        active_dasha_hierarchy = None
        transit_snapshot = None
        panchanga = None
        muhurta_suite = None
        timing_suite = None
        temporal_hash = None

        if query_dt:
            # Active Dasha hierarchy at query_dt
            query_dasha_suite = DashaEngine.calculate_dasha_suite(canonical_chart, query_dt)
            active_dasha_hierarchy = query_dasha_suite.active_hierarchy

            active_md = active_dasha_hierarchy.mahadasha.lord_planet
            active_ad = active_dasha_hierarchy.antardasha.lord_planet if active_dasha_hierarchy.antardasha else None

            # Section 3 Compliance: Zero planet fallbacks!
            active_lords = {"Mahadasha": active_md}
            if active_ad:
                active_lords["Antardasha"] = active_ad

            transit_snapshot = TransitEngine.calculate_transit_snapshot(
                natal_chart=canonical_chart,
                query_dt=query_dt,
                astronomy_provider=astronomy_provider,
                active_dasha_lords=active_lords
            )

            panchanga = PanchangaEngine.calculate_panchanga(
                dt=query_dt,
                latitude=birth_input.latitude,
                longitude=birth_input.longitude,
                location_name=birth_input.name,
                astronomy_provider=astronomy_provider
            )

            muhurta_suite = MuhurtaEngine.evaluate_all_activities(
                dt=query_dt,
                latitude=birth_input.latitude,
                longitude=birth_input.longitude,
                location_name=birth_input.name,
                astronomy_provider=astronomy_provider
            )

            timing_suite = TimingEngine.generate_timing_suite(canonical_chart, query_dt)

            temp_payload = {
                "natal_hash": natal_hash,
                "query_iso": query_dt.isoformat(),
                "active_dasha_md": active_md,
                "active_dasha_ad": active_ad or "NONE",
                "transit_hash": transit_snapshot.calculation_hash,
                "panchanga_hash": panchanga.calculation_hash,
                "timing_hash": timing_suite.calculation_hash
            }
            temporal_hash = hashlib.sha256(json.dumps(temp_payload, sort_keys=True).encode("utf-8")).hexdigest()

        # Master Evidence Hash
        master_payload = {
            "natal_hash": natal_hash,
            "temporal_hash": temporal_hash or "NATAL_ONLY"
        }
        master_hash = hashlib.sha256(json.dumps(master_payload, sort_keys=True).encode("utf-8")).hexdigest()

        return CanonicalAstrologyEvidence(
            birth_input=birth_input,
            canonical_chart=canonical_chart,
            varga_suite=varga_suite,
            varga_evidence=varga_evidence,
            natal_dasha_suite=natal_dasha_suite,
            active_dasha_hierarchy=active_dasha_hierarchy,
            yoga_suite=yoga_suite,
            dosha_suite=dosha_suite,
            shadbala_suite=shadbala_suite,
            shadbala_evidence=shadbala_evidence,
            ashtakavarga_suite=ashtakavarga_suite,
            ashtakavarga_evidence=ashtakavarga_evidence,
            jaimini_suite=jaimini_suite,
            transit_snapshot=transit_snapshot,
            panchanga=panchanga,
            muhurta_suite=muhurta_suite,
            timing_suite=timing_suite,
            natal_calculation_hash=natal_hash,
            temporal_calculation_hash=temporal_hash,
            master_evidence_hash=master_hash
        )
