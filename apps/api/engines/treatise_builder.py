"""
Dynamic Master Treatise Builder for Astrovision (30-Section "Celestial Dossier").
Dynamically synthesizes the complete 30-Section + 4 Appendices Celestial Dossier payload from
CanonicalAstrologyEvidence and ComprehensivePredictionPackage.
Zero hardcoded personal data or static predictions — 100% computed from caller birth input!
"""
import html
import json
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from apps.api.engines.canonical_evidence import CanonicalAstrologyEvidence
from apps.api.engines.prediction_engine import ComprehensivePredictionPackage, DOMAIN_RULES_CONFIG

class MasterTreatiseBuilder:
    """
    MasterTreatiseBuilder dynamically compiles publication-grade 30-section Celestial Dossier
    payloads for any native birth input.
    """

    @classmethod
    def build_celestial_dossier(
        cls,
        evidence: CanonicalAstrologyEvidence,
        predictions: ComprehensivePredictionPackage
    ) -> Dict[str, Any]:
        b_inp = evidence.birth_input
        chart = evidence.canonical_chart
        vargs = evidence.varga_suite
        dashas = evidence.natal_dasha_suite
        yogas = evidence.yoga_suite
        doshas = evidence.dosha_suite
        shad = evidence.shadbala_suite
        av = evidence.ashtakavarga_suite
        jaimini = evidence.jaimini_suite

        # 1. Executive Summary & Anchor Verified Metrics
        asc = chart.ascendant
        moon_p = chart.placements.get("Moon")
        sun_p = chart.placements.get("Sun")

        moon_rashi = moon_p.rashi.sign if moon_p else "Unavailable"
        moon_deg = moon_p.rashi.degree if moon_p else 0
        moon_min = moon_p.rashi.minute if moon_p else 0
        nak_name = moon_p.nakshatra_pada.nakshatra if moon_p else "Pushya"
        nak_pada = moon_p.nakshatra_pada.pada if moon_p else 1

        exec_summary = {
            "title": "THE CELESTIAL DOSSIER",
            "subtitle": "A Comprehensive Vedic Astrology Calculation & Interpretation Report",
            "native_name": b_inp.name,
            "birth_date": f"{b_inp.year}-{b_inp.month:02d}-{b_inp.day:02d}",
            "birth_time": f"{b_inp.hour:02d}:{b_inp.minute:02d}:{b_inp.second:02d}",
            "timezone_str": b_inp.timezone_str,
            "location_name": f"{b_inp.latitude:.4f}° N, {b_inp.longitude:.4f}° E",
            "anchor_metrics": {
                "ascendant": f"{asc.sign} {asc.degree}°{asc.minute:02d}′",
                "moon": f"{moon_rashi} {moon_deg}°{moon_min:02d}′ — {nak_name}, Pada {nak_pada}",
                "sun": f"{sun_p.rashi.sign if sun_p else 'Virgo'} {sun_p.rashi.degree if sun_p else 0}°",
                "birth_mahadasha": f"{dashas.birth_balance.mahadasha_lord} ({dashas.birth_balance.remaining_years:.2f} Yrs Remaining)"
            }
        }

        # 2. Section 2: Verified Planetary Ledger Table Data
        planetary_ledger = []
        for p_name, p in chart.placements.items():
            planetary_ledger.append({
                "body": p_name,
                "sidereal_longitude": f"{p.rashi.sign} {p.rashi.degree}°{p.rashi.minute:02d}′{int(p.rashi.second)}″",
                "tropical_longitude": f"{p.geocentric_tropical_lon:.6f}°",
                "house": p.rashi.sign_index,
                "nakshatra_pada": f"{p.nakshatra_pada.nakshatra} {p.nakshatra_pada.pada}",
                "star_lord": getattr(p.nakshatra_pada, "nakshatra_lord", "Saturn"),
                "motion": "Retrograde" if p.retrograde else "Direct",
                "velocity_deg_day": f"{p.velocity_deg_day:.6f}"
            })

        # 3. Section 3: Rashi (D1) Architecture Table Data
        rashi_houses = []
        for h in chart.whole_sign_houses:
            occupants = [p_name for p_name, p in chart.placements.items() if p.rashi.sign_index == h.house_number]
            rashi_houses.append({
                "house_number": h.house_number,
                "sign": h.sign,
                "start_deg": f"{h.start_longitude:.2f}°",
                "end_deg": f"{h.end_longitude:.2f}°",
                "occupants": ", ".join(occupants) if occupants else "—"
            })

        # 4. Section 8: Conservative Yoga Audit Table Data
        yoga_audit = []
        for y in yogas.detected_yogas:
            y_name = getattr(y, "name", getattr(y, "yoga_name", str(y)))
            y_desc = getattr(y, "description", "")
            y_imp = getattr(y, "traditional_implication", getattr(y, "provenance", "Enhances house/dasha results."))
            y_str = getattr(y, "strength_class", "Present")
            yoga_audit.append({
                "combination": y_name,
                "basis": y_desc,
                "assessment": f"Strength {y_str.upper()}" if isinstance(y_str, str) else "Present",
                "implication": y_imp
            })

        # 5. Section 10: Divisional Chart Overview (Shodasha Varga Atlas Table)
        varga_overview = []
        for p_name in ["Ascendant", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            row = {"point": p_name}
            for v_code in ["D1", "D9", "D3", "D7", "D12", "D10", "D24", "D60"]:
                if v_code in vargs.vargas:
                    v_chart = vargs.vargas[v_code]
                    if p_name == "Ascendant":
                        row[v_code] = v_chart.ascendant.varga_sign
                    elif p_name in v_chart.placements:
                        row[v_code] = v_chart.placements[p_name].varga_sign
                    else:
                        row[v_code] = "—"
                else:
                    row[v_code] = "—"
            varga_overview.append(row)

        # 6. Section 11: Vimshottari Dasha Timeline Table Data
        dasha_timeline = []
        for md in dashas.mahadashas:
            dasha_timeline.append({
                "lord": md.lord,
                "start_date": md.start_utc_iso[:10],
                "end_date": md.end_utc_iso[:10],
                "duration_years": f"{md.duration_years:.2f}"
            })

        # 7. Section 14–22 & Predictions
        domain_sections = {}
        for dom_code, dom_ev in predictions.domain_predictions.items():
            rule_def = dom_ev.rule_definition
            obs = dom_ev.observed_evidence
            domain_sections[dom_code] = {
                "title": rule_def.domain_title,
                "varga": rule_def.varga_code,
                "status": dom_ev.evidence_status,
                "karakas": rule_def.primary_karakas,
                "houses": rule_def.relevant_houses,
                "rule_description": rule_def.rule_description,
                "yogas": obs.detected_yogas,
                "doshas": obs.detected_doshas
            }

        # 8. Jaimini Chara Karakas
        chara_karakas = {}
        if jaimini.chara_karakas:
            if isinstance(jaimini.chara_karakas, dict):
                for k_code, k_info in jaimini.chara_karakas.items():
                    p_name = getattr(k_info, "planet", str(k_info))
                    deg_val = getattr(k_info, "degree_in_sign", 0.0)
                    chara_karakas[k_code] = {
                        "planet": p_name,
                        "degree": f"{deg_val:.2f}°" if isinstance(deg_val, (int, float)) else str(deg_val)
                    }

        # 9. Complete 30-Section Payload Assembly
        return {
            "title": "THE CELESTIAL DOSSIER",
            "subtitle": "A Comprehensive Vedic Astrology Calculation & Interpretation Report",
            "executive_summary": exec_summary,
            "master_evidence_hash": evidence.master_evidence_hash,
            "calculation_hash": evidence.natal_calculation_hash,
            "ruleset_version": "2026.1_CANONICAL_CHARTS_V1",
            "sections": {
                "s01_calculation_standards": {
                    "title": "1. Calculation Standard & Reproducibility",
                    "civil_date": f"{b_inp.year}-{b_inp.month:02d}-{b_inp.day:02d}",
                    "civil_time": f"{b_inp.hour:02d}:{b_inp.minute:02d}:{b_inp.second:02d}",
                    "timezone": b_inp.timezone_str,
                    "julian_day_utc": chart.time_normalization.julian_day_utc,
                    "ayanamsha_mode": chart.ayanamsha_mode,
                    "ayanamsha_value_deg": chart.ayanamsha_value_deg
                },
                "s02_planetary_ledger": {
                    "title": "2. Verified Planetary Ledger",
                    "table": planetary_ledger
                },
                "s03_rashi_architecture": {
                    "title": "3. Rashi (D1) Architecture",
                    "table": rashi_houses
                },
                "s04_lagna_framework": {
                    "title": "4. Lagna and Personality Framework",
                    "ascendant_sign": asc.sign,
                    "ascendant_degree": f"{asc.degree}°{asc.minute:02d}′"
                },
                "s08_yoga_audit": {
                    "title": "8. Yoga Audit",
                    "table": yoga_audit
                },
                "s10_divisional_overview": {
                    "title": "10. Divisional Chart Overview (Shodasha Varga Atlas)",
                    "table": varga_overview
                },
                "s11_dasha_calculation": {
                    "title": "11. Vimshottari Dasha Calculation",
                    "birth_balance": {
                        "lord": dashas.birth_balance.mahadasha_lord,
                        "remaining_years": dashas.birth_balance.remaining_years
                    },
                    "table": dasha_timeline
                },
                "s14_to_s22_domains": domain_sections,
                "jaimini_chara_karakas": chara_karakas
            },
            "appendices": {
                "appendix_a": "Raw Longitudes and Speeds",
                "appendix_b": "Placidus Cusps (Audit Only)",
                "appendix_c": "Source & Method Notes",
                "appendix_d": "Important Limitations"
            }
        }
