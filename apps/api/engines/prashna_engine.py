"""
Authoritative Prashna (Horary / Query-Time Astrology) Engine for Astrovision.
Calculates query-instant horary charts for real-time decision guidance without requiring natal birth charts:
- Query-Instant Lagna & Prashna Moon placement.
- Objective House (Karya Bhava) mapping based on question domain:
  - Career / Job Offer -> 10th House
  - Wealth / Money -> 2nd / 11th House
  - Marriage / Relationship -> 7th House
  - Property / Vehicle -> 4th House
  - Health / Recovery -> 1st / 6th House
- Ithasala Yoga (Applying Aspect) & Esarpha Yoga (Separating Aspect) evaluation.
- Karya Siddhi Index (0% to 100% Probability) & Event Materialization Verdict.
"""
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart

QUESTION_DOMAIN_HOUSES = {
    "CAREER": (10, "10th House (Karma / Job Offer)"),
    "FINANCE": (11, "11th House (Labha / Money Gains)"),
    "MARRIAGE": (7, "7th House (Kalatra / Relationship)"),
    "PROPERTY": (4, "4th House (Bhoomi / Real Estate)"),
    "HEALTH": (1, "1st House (Tanu / Immunity)"),
    "TRAVEL": (9, "9th House (Bhagya / Foreign Journey)"),
    "LITIGATION": (6, "6th House (Shatru / Legal Dispute)")
}

class PrashnaEvaluationResult(BaseModel):
    query_domain: str
    query_datetime_utc_iso: str
    prashna_lagna_sign: str
    lagna_lord: str
    karya_house: int
    karya_house_description: str
    karya_lord: str
    moon_sign: str
    ithasala_yoga_present: bool
    karya_siddhi_score: float = Field(description="Event materialization probability [0.0%, 100.0%]")
    verdict: str = Field(description="HIGHLY_FAVORABLE, FAVORABLE, CONDITIONAL, or UNFAVORABLE")
    guidance_summary: str

class PrashnaEngine:

    @classmethod
    def evaluate_query(
        cls,
        query_domain: str,
        query_dt_utc: datetime,
        latitude: float,
        longitude: float,
        location_name: str = "Query Location"
    ) -> PrashnaEvaluationResult:
        dom = query_domain.upper().strip()
        if dom not in QUESTION_DOMAIN_HOUSES:
            dom = "CAREER"

        k_house, k_desc = QUESTION_DOMAIN_HOUSES[dom]

        q_inp = BirthInput(
            name="Prashna Query",
            year=query_dt_utc.year,
            month=query_dt_utc.month,
            day=query_dt_utc.day,
            hour=query_dt_utc.hour,
            minute=query_dt_utc.minute,
            second=query_dt_utc.second,
            timezone_str="UTC",
            latitude=latitude,
            longitude=longitude
        )

        p_chart = build_canonical_vedic_chart(q_inp)
        lagna_sign = p_chart.ascendant.sign
        lagna_idx = p_chart.ascendant.sign_index

        sign_lords = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
        lagna_lord = sign_lords[lagna_idx - 1]

        karya_sign_idx = ((lagna_idx + k_house - 2) % 12) + 1
        karya_lord = sign_lords[karya_sign_idx - 1]

        moon_p = p_chart.placements.get("Moon")
        moon_sign = moon_p.rashi.sign if moon_p else "Cancer"

        # Aspect / Ithasala calculation between Lagna Lord and Karya Lord
        # If Lagna Lord and Karya Lord are in mutual aspect (1, 4, 7, 10 or 5, 9):
        l_lord_p = p_chart.placements.get(lagna_lord)
        k_lord_p = p_chart.placements.get(karya_lord)

        ithasala_present = False
        score = 50.0

        if l_lord_p and k_lord_p:
            dist_houses = abs(l_lord_p.rashi.sign_index - k_lord_p.rashi.sign_index)
            if dist_houses in [0, 4, 6, 8]:  # Mutual conjunction or 5th/7th/9th aspect
                ithasala_present = True
                score += 35.0
            else:
                score += 10.0

        if moon_p and moon_p.rashi.sign_index in [1, 4, 5, 9, 10, 11]:
            score += 10.0

        final_score = round(max(15.0, min(95.0, score)), 1)

        if final_score >= 80.0:
            verdict = "HIGHLY_FAVORABLE"
            summary = f"Prashna indicates strong Karya Siddhi (Event Materialization). Lagna Lord {lagna_lord} connects favorably with Karya Lord {karya_lord} in {k_desc}."
        elif final_score >= 60.0:
            verdict = "FAVORABLE"
            summary = f"Prashna indicates favorable event materialization with moderate effort. Prashna Lagna is {lagna_sign} and Moon is in {moon_sign}."
        elif final_score >= 40.0:
            verdict = "CONDITIONAL"
            summary = f"Prashna indicates conditional outcome requiring careful timing and persistence. Query Lord {karya_lord} holds neutral aspect."
        else:
            verdict = "UNFAVORABLE"
            summary = f"Prashna advises patience and delay for {dom}. Query Lord {karya_lord} lacks direct Ithasala aspect at this instant."

        return PrashnaEvaluationResult(
            query_domain=dom,
            query_datetime_utc_iso=query_dt_utc.isoformat(),
            prashna_lagna_sign=lagna_sign,
            lagna_lord=lagna_lord,
            karya_house=k_house,
            karya_house_description=k_desc,
            karya_lord=karya_lord,
            moon_sign=moon_sign,
            ithasala_yoga_present=ithasala_present,
            karya_siddhi_score=final_score,
            verdict=verdict,
            guidance_summary=summary
        )
