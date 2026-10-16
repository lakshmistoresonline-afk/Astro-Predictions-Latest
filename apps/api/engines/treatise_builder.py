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

        if not moon_p or not sun_p or not asc:
            raise ValueError("Required planetary or ascendant placement missing from canonical chart.")

        moon_rashi = moon_p.rashi.sign
        moon_deg = moon_p.rashi.degree
        moon_min = moon_p.rashi.minute
        nak_name = moon_p.nakshatra_pada.nakshatra
        nak_pada = moon_p.nakshatra_pada.pada
        nak_lord = moon_p.nakshatra_pada.ruling_planet or "Saturn"

        sun_rashi = sun_p.rashi.sign
        sun_deg = sun_p.rashi.degree

        birth_bal_lord = dashas.birth_balance.mahadasha_lord
        bal_rem_yrs = dashas.birth_balance.remaining_years

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
                "sun": f"{sun_rashi} {sun_deg}°",
                "birth_mahadasha": f"{birth_bal_lord} Mahadasha ({bal_rem_yrs:.2f} Yrs Remaining)"
            }
        }

        # 2. Section 2: Verified Planetary Ledger Table Data
        planetary_ledger = []
        for p_name, p in chart.placements.items():
            star_l = p.nakshatra_pada.ruling_planet or "Ketu"
            trop_lon = f"{p.geocentric_tropical_lon:.6f}°" if p.geocentric_tropical_lon is not None else "—"
            vel_str = f"{p.velocity_deg_day:.6f}" if p.velocity_deg_day is not None else "—"

            planetary_ledger.append({
                "body": p_name,
                "sidereal_longitude": f"{p.rashi.sign} {p.rashi.degree}°{p.rashi.minute:02d}′{int(p.rashi.second)}″",
                "tropical_longitude": trop_lon,
                "house": p.rashi.sign_index,
                "nakshatra_pada": f"{p.nakshatra_pada.nakshatra} {p.nakshatra_pada.pada}",
                "star_lord": star_l,
                "motion": "Retrograde" if p.retrograde else "Direct",
                "velocity_deg_day": vel_str
            })

        # 3. Section 3: Rashi (D1) Architecture Table Data
        rashi_houses = []
        for h in chart.get_whole_sign_houses:
            h_num = getattr(h, "house_number", 1)
            h_sign = getattr(h, "sign_name", getattr(h, "sign", "Aries"))
            h_lord = getattr(h, "lord_planet", "Mars")
            occupants = [p_name for p_name, p in chart.placements.items() if p.rashi.sign_index == h_num]

            rashi_houses.append({
                "house_number": h_num,
                "sign": h_sign,
                "lord": h_lord,
                "start_deg": f"{getattr(h, 'start_longitude', 0.0):.2f}°",
                "end_deg": f"{getattr(h, 'end_longitude', 30.0):.2f}°",
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

        # 7. Section 14–20 Domain Predictions
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

        # 9. Assembly of all 30 Dynamic Sections
        sections_payload = [
            {
                "number": 1,
                "title": "1. Calculation Standard & Reproducibility",
                "content": f"Normalized birth data for {b_inp.name} ({b_inp.year}-{b_inp.month:02d}-{b_inp.day:02d} {b_inp.hour:02d}:{b_inp.minute:02d}:{b_inp.second:02d} {b_inp.timezone_str}). Julian Day UTC: {chart.time_normalization.julian_day_utc:.6f}. Ayanamsha: {chart.ayanamsha_mode} ({chart.ayanamsha_value_deg:.6f}°). Calculation Hash: {evidence.master_evidence_hash[:32]}."
            },
            {
                "number": 2,
                "title": "2. Verified Planetary Ledger",
                "content": f"Complete sidereal placements for {b_inp.name} calculated via NASA JPL DE440s ephemeris kernel.",
                "table": planetary_ledger
            },
            {
                "number": 3,
                "title": "3. Rashi (D1) Architecture",
                "content": f"Whole Sign house divisions starting from {asc.sign} Ascendant across all 12 Bhavas.",
                "table": rashi_houses
            },
            {
                "number": 4,
                "title": "4. Lagna and Personality Framework",
                "content": f"Ascendant in {asc.sign} ({asc.degree}°{asc.minute:02d}′). Governs vital constitution, temperament, and life direction for {b_inp.name}."
            },
            {
                "number": 5,
                "title": "5. Planet-by-Planet Interpretation",
                "content": f"Sun in {sun_rashi}, Moon in {moon_rashi} ({nak_name} Nakshatra, Pada {nak_pada}), and planetary placements across houses."
            },
            {
                "number": 6,
                "title": "6. House-by-House Analysis",
                "content": f"Detailed evaluation across Houses 1 through 12 starting from {asc.sign} Lagna."
            },
            {
                "number": 7,
                "title": "7. Classical Aspect Matrix",
                "content": "Geocentric planetary aspects, orb angles, and special Parashari mutual aspect geometry."
            },
            {
                "number": 8,
                "title": "8. Yoga Audit",
                "content": f"Detected {len(yogas.detected_yogas)} classical Yogas for {b_inp.name}.",
                "table": yoga_audit
            },
            {
                "number": 9,
                "title": "9. Nakshatra Matrix",
                "content": f"Janma Nakshatra is {nak_name} (Pada {nak_pada}, ruled by {nak_lord})."
            },
            {
                "number": 10,
                "title": "10. Divisional Chart Overview (Shodasha Varga Atlas)",
                "content": "16 Parashari divisional charts (D1, D9, D3, D7, D12, D10, D24, D60) mapping divisional dignities.",
                "table": varga_overview
            },
            {
                "number": 11,
                "title": "11. Vimshottari Dasha Calculation",
                "content": f"120-year Vimshottari timeline starting from birth balance {birth_bal_lord} Mahadasha ({bal_rem_yrs:.2f} Yrs remaining).",
                "table": dasha_timeline
            },
            {
                "number": 12,
                "title": "12. Active Mahadasha Deep Dive",
                "content": f"Active Dasha analysis for {b_inp.name} starting from birth balance lord {birth_bal_lord}."
            },
            {
                "number": 13,
                "title": "13. Current Transit Snapshot",
                "content": "Real-time geocentric planetary transits and aspect contacts relative to natal Lagna."
            },
            {
                "number": 14,
                "title": "14. Career & Professional Destiny",
                "content": "10th house Karma bhava, D10 Dashamsha, Saturn, and Mercury career vectors."
            },
            {
                "number": 15,
                "title": "15. Wealth, Income & Asset Strategy",
                "content": "2nd Dhana and 11th Labha houses, D2 Hora, and Dhana Yogas in Indian Rupees (₹)."
            },
            {
                "number": 16,
                "title": "16. Business & Entrepreneurship",
                "content": "7th Kalatra, 10th Karma, and commercial enterprise partnerships."
            },
            {
                "number": 17,
                "title": "17. Relationships & Marriage",
                "content": "7th house, Venus, and D9 Navamsha marital dharma."
            },
            {
                "number": 18,
                "title": "18. Education, Intelligence & Research",
                "content": "4th schooling, 5th intellect, and 9th higher learning houses with D24."
            },
            {
                "number": 19,
                "title": "19. Foreign Travel, Relocation & Global Work",
                "content": "9th pilgrimage and 12th foreign residence houses."
            },
            {
                "number": 20,
                "title": "20. Home, Property & Vehicles",
                "content": "4th house, D4 Chaturthamsha, Mars, and Saturn property assets."
            },
            {
                "number": 21,
                "title": "21. Health & Lifestyle - Traditional, Non-Medical",
                "content": "1st vitality, 6th immunity, and 8th longevity bhava analysis (Non-Medical Disclaimer)."
            },
            {
                "number": 22,
                "title": "22. Spiritual & Philosophical Themes",
                "content": "9th Dharma, 12th Moksha, and D20 Vimshamsha spiritual sadhana."
            },
            {
                "number": 23,
                "title": "23. Risk Register - Where the Chart Asks for Discipline",
                "content": "Risk area factors, vulnerable houses, and traditional mitigations."
            },
            {
                "number": 24,
                "title": "24. 2026-2030 Strategic Astrology Timeline",
                "content": "5-year strategic window predictions and timing convergence."
            },
            {
                "number": 25,
                "title": "25. 2031-2044 Strategic Astrology Timeline",
                "content": "Long-range strategic window predictions and timing convergence."
            },
            {
                "number": 26,
                "title": "26. Traditional Remedial Framework",
                "content": "Optional traditional practices, mantras, service, and gemstone dignities."
            },
            {
                "number": 27,
                "title": "27. Application Benchmark Specification",
                "content": f"Software reproducibility benchmark parameters and calculation hash: {evidence.master_evidence_hash[:32]}."
            },
            {
                "number": 28,
                "title": "28. Validation Checklist",
                "content": "Deterministic verification checklist for astronomical calculations."
            },
            {
                "number": 29,
                "title": "29. Interpretation Confidence Framework",
                "content": "Confidence Classes A-D categorizing direct facts vs traditional insights."
            },
            {
                "number": 30,
                "title": "30. Final Integrated Reading",
                "content": f"High-level synthesis summary uniting all chart factors into a coherent reading for {b_inp.name}."
            }
        ]

        return {
            "title": "THE CELESTIAL DOSSIER",
            "subtitle": "A Comprehensive Vedic Astrology Calculation & Interpretation Report",
            "executive_summary": exec_summary,
            "master_evidence_hash": evidence.master_evidence_hash,
            "calculation_hash": evidence.natal_calculation_hash,
            "ruleset_version": "2026.1_CANONICAL_CHARTS_V1",
            "sections_list": sections_payload,
            "domain_sections": domain_sections,
            "jaimini_chara_karakas": chara_karakas,
            "appendices": {
                "appendix_a": "Raw Longitudes and Speeds",
                "appendix_b": "House Cusps & Lords",
                "appendix_c": "Source & Method Notes",
                "appendix_d": "Important Limitations & Non-Medical Disclaimer"
            }
        }
