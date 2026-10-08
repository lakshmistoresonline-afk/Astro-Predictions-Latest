"""
Authoritative Predictive Timing Window Engine for Astrovision.
Section 1..10 Compliance:
- Zero arbitrary scoring model! Evidence-driven timing window synthesis.
- Requires query_dt; if query_dt is None, returns structured TimingSuiteResult with evidence_status="UNAVAILABLE".
- Normalizes query_dt to UTC before timing calculations.
- Creates TimingWindow objects ONLY when actual Dasha or Transit convergence exists for that domain.
- relevant_planets contains ONLY planets actually involved in the timing event (Dasha lords, transiting Jupiter).
- Domain-scoped Yoga filtering (only Yogas involving domain karakas are attached!).
- Nullable end date (zero manufactured 180-day windows!).
- Uses actual natal Ashtakavarga SAV bindus via AshtakavargaEngine.
- 100% Deterministic timing window IDs and calculation hashes derived from SHA-256 over serialized window payloads.
"""
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional

from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.dasha.engine import DashaEngine
from apps.api.engines.transit.engine import TransitEngine
from apps.api.engines.yogas.evaluator import YogaEvaluator
from apps.api.engines.strength.ashtakavarga import AshtakavargaEngine
from apps.api.engines.timing.models import TimingWindow, TimingSuiteResult

TIMING_RULESET_VERSION = "2026.1_PARASHARI_CONVERGENCE_V1"

DOMAIN_HOUSES_MAP = {
    "CAREER": ([10, 1, 6, 11], ["D10", "D1"], ["Sun", "Saturn", "Jupiter", "Mercury"]),
    "FINANCE": ([2, 11, 5, 9], ["D2", "D1"], ["Jupiter", "Venus", "Mercury"]),
    "BUSINESS": ([7, 10, 11], ["D10", "D2"], ["Mercury", "Mars", "Venus"]),
    "MARRIAGE": ([7, 1, 5], ["D9", "D1"], ["Venus", "Jupiter"]),
    "RELATIONSHIP": ([5, 7], ["D9", "D1"], ["Venus", "Moon"]),
    "EDUCATION": ([4, 5, 9], ["D24", "D1"], ["Mercury", "Jupiter"]),
    "FAMILY": ([2, 4], ["D12", "D1"], ["Moon", "Jupiter"]),
    "CHILDREN": ([5, 9], ["D7", "D1"], ["Jupiter", "Mars"]),
    "PROPERTY": ([4, 11], ["D4", "D1"], ["Mars", "Saturn"]),
    "TRAVEL": ([9, 12, 7], ["D1", "D9"], ["Moon", "Rahu", "Jupiter"]),
    "RELOCATION": ([4, 12, 9], ["D4", "D1"], ["Moon", "Saturn"]),
    "SPIRITUALITY": ([9, 12, 5], ["D20", "D9"], ["Jupiter", "Ketu", "Sun"]),
    "PERSONAL_DEVELOPMENT": ([1, 5, 9], ["D1", "D60"], ["Sun", "Moon", "Mars"]),
    "WELLBEING": ([1, 6, 8], ["D1", "D30"], ["Sun", "Moon", "Mars"])
}

class TimingEngine:
    """
    Authoritative Predictive Timing Window Engine.
    Identifies windows of convergent astrological indicators across domains for an explicit query_dt.
    """

    @classmethod
    def generate_timing_suite(
        cls,
        natal_chart: CanonicalVedicChart,
        query_dt: Optional[datetime] = None
    ) -> TimingSuiteResult:
        if not query_dt:
            payload = {
                "natal_hash": natal_chart.calculation_hash,
                "evidence_status": "UNAVAILABLE",
                "ruleset": TIMING_RULESET_VERSION
            }
            unavail_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()
            return TimingSuiteResult(
                chart_hash=natal_chart.calculation_hash,
                query_datetime_iso=None,
                evidence_status="UNAVAILABLE",
                active_mahadasha="UNAVAILABLE",
                active_antardasha=None,
                ruleset_version=TIMING_RULESET_VERSION,
                timing_windows=[],
                calculation_hash=unavail_hash
            )

        if query_dt.tzinfo is None:
            query_dt = query_dt.replace(tzinfo=timezone.utc)

        utc_dt = query_dt.astimezone(timezone.utc)

        # 1. Calculate Dasha timeline at explicit query_dt
        dasha_suite = DashaEngine.calculate_dasha_suite(natal_chart, utc_dt)
        active_hier = dasha_suite.active_hierarchy

        md_lord = active_hier.mahadasha.lord_planet
        ad_lord = active_hier.antardasha.lord_planet if active_hier.antardasha else None
        pd_lord = active_hier.pratyantardasha.lord_planet if active_hier.pratyantardasha else None
        sd_lord = active_hier.sookshma.lord_planet if active_hier.sookshma else None
        pr_lord = active_hier.prana.lord_planet if active_hier.prana else None

        # 2. Calculate Active Transit Snapshot at explicit query_dt
        active_dasha_map = {"Mahadasha": md_lord}
        if ad_lord:
            active_dasha_map["Antardasha"] = ad_lord
        if pd_lord:
            active_dasha_map["Pratyantardasha"] = pd_lord

        transit_snap = TransitEngine.calculate_transit_snapshot(
            natal_chart=natal_chart,
            query_dt=utc_dt,
            active_dasha_lords=active_dasha_map
        )

        # 3. Yogas
        yoga_suite = YogaEvaluator.evaluate_all_yogas(natal_chart)

        # 4. Calculate Live Natal Ashtakavarga SAV Bindus
        natal_av = AshtakavargaEngine.calculate_ashtakavarga(natal_chart)

        # 5. Generate Domain Timing Windows
        windows: List[TimingWindow] = []

        for domain, (houses, v_codes, primary_p) in DOMAIN_HOUSES_MAP.items():
            dasha_match = (md_lord in primary_p) or (ad_lord is not None and ad_lord in primary_p)

            trans_jup_place = transit_snap.placements.get("Jupiter")
            trans_jupiter_house = trans_jup_place.house_from_lagna if trans_jup_place else None

            transit_match = (trans_jupiter_house is not None and trans_jupiter_house in houses)

            if not (dasha_match or transit_match):
                continue

            active_event_planets = []
            if md_lord in primary_p:
                active_event_planets.append(md_lord)
            if ad_lord and ad_lord in primary_p and ad_lord not in active_event_planets:
                active_event_planets.append(ad_lord)
            if transit_match and "Jupiter" not in active_event_planets:
                active_event_planets.append("Jupiter")

            domain_yogas = [
                y.name for y in yoga_suite.detected_yogas
                if any(p in primary_p for p in y.participating_planets)
            ]

            if trans_jupiter_house is not None and natal_av and natal_av.sav and len(natal_av.sav.bindus) >= 12:
                lagna_r_idx = natal_chart.ascendant.rashi.rashi_index
                trans_r_idx = ((lagna_r_idx + trans_jupiter_house - 2) % 12) + 1
                sav_bindus_val = natal_av.sav.bindus[trans_r_idx - 1]
                sav_evidence_text = f"House {trans_jupiter_house} ({natal_chart.houses[trans_jupiter_house - 1].rashi.name_english}) SAV: {sav_bindus_val} bindus"
            else:
                sav_evidence_text = "Ashtakavarga SAV data unavailable"

            if dasha_match and transit_match:
                evidence_status = "CONVERGENT"
                strength_cls = "HIGH"
            elif dasha_match or transit_match:
                evidence_status = "PARTIAL"
                strength_cls = "MODERATE"
            else:
                evidence_status = "UNAVAILABLE"
                strength_cls = None

            start_iso = active_hier.antardasha.start_datetime_iso if active_hier.antardasha else utc_dt.isoformat()
            end_iso = active_hier.antardasha.end_datetime_iso if active_hier.antardasha else None

            ad_desc = f"-{ad_lord}" if ad_lord else ""
            jup_desc = f"Jupiter transit in House {trans_jupiter_house}" if trans_jupiter_house is not None else "Jupiter transit location unavailable"

            summary = (
                f"Timing window for {domain} (Start: {start_iso[:10]}): "
                f"Activated by {md_lord}{ad_desc} Dasha and {jup_desc}. "
                f"Status: {evidence_status}."
            )

            id_payload = f"{natal_chart.calculation_hash}_{utc_dt.isoformat()}_{domain}_{start_iso}_{end_iso or 'NONE'}_{md_lord}_{ad_lord or 'NONE'}_{pd_lord or 'NONE'}_{sd_lord or 'NONE'}_{pr_lord or 'NONE'}_{TIMING_RULESET_VERSION}"
            w_hash = hashlib.sha256(id_payload.encode("utf-8")).hexdigest()[:12]
            window_id = f"TW_{domain}_{w_hash}"

            windows.append(TimingWindow(
                window_id=window_id,
                domain=domain,
                start_datetime_iso=start_iso,
                end_datetime_iso=end_iso,
                mahadasha_lord=md_lord,
                antardasha_lord=ad_lord,
                pratyantardasha_lord=pd_lord,
                sookshma_lord=sd_lord,
                prana_lord=pr_lord,
                relevant_planets=active_event_planets,
                relevant_houses=houses,
                supporting_vargas=v_codes,
                supporting_yogas=domain_yogas,
                active_transits_summary=jup_desc,
                ashtakavarga_support=sav_evidence_text,
                evidence_status=evidence_status,
                evidence_strength_class=strength_cls,
                description=summary
            ))

        windows_serialized = [w.model_dump() for w in windows]
        payload = {
            "natal_hash": natal_chart.calculation_hash,
            "md": md_lord,
            "ad": ad_lord or "NONE",
            "pd": pd_lord or "NONE",
            "sd": sd_lord or "NONE",
            "pr": pr_lord or "NONE",
            "query_iso": utc_dt.isoformat(),
            "transit_hash": transit_snap.calculation_hash,
            "windows": windows_serialized,
            "ruleset": TIMING_RULESET_VERSION
        }
        calc_hash = hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()

        return TimingSuiteResult(
            chart_hash=natal_chart.calculation_hash,
            query_datetime_iso=utc_dt.isoformat(),
            evidence_status="AVAILABLE",
            active_mahadasha=md_lord,
            active_antardasha=ad_lord,
            ruleset_version=TIMING_RULESET_VERSION,
            timing_windows=windows,
            calculation_hash=calc_hash
        )

TimingEngine.evaluate_timing_suite = TimingEngine.generate_timing_suite
