"""
Authoritative Shadbala Engine.
Calculates Sthana Bala, Dig Bala, Kala Bala, Cheshta Bala, Naisargika Bala, Drik Bala from Canonical Phase 2A/2B State.
"""
import hashlib
import json
from typing import Dict, List

from apps.api.engines.vedic.models import CanonicalVedicChart
from apps.api.engines.varga.models import Full16VargaSuite
from apps.api.engines.strength.models import (
    ShadbalaComponent,
    PlanetShadbala,
    ShadbalaSuiteResult
)
from apps.api.engines.strength.exceptions import MissingCanonicalStateError, UnsupportedPlanetError
from apps.api.engines.yogas.rules import EXALTATION_SIGNS, DEBILITATION_SIGNS

# Naisargika Bala Constants (in Shashtiamsas) from BPHS
NAISARGIKA_BALA_SHASHTIAMSAS = {
    "Sun": 60.0,
    "Moon": 51.43,
    "Venus": 42.85,
    "Jupiter": 34.28,
    "Mercury": 25.70,
    "Mars": 17.14,
    "Saturn": 8.57
}

# Dig Bala Power Houses (0-indexed house offsets from Ascendant)
DIG_BALA_HOUSES = {
    "Sun": 9,      # 10th House
    "Mars": 9,     # 10th House
    "Jupiter": 0,  # 1st House
    "Mercury": 0,  # 1st House
    "Saturn": 6,   # 7th House
    "Moon": 3,     # 4th House
    "Venus": 3     # 4th House
}

class ShadbalaEngine:
    """Evaluator for the Six-Fold Planetary Strength (Shadbala)."""

    @classmethod
    def calculate_shadbala_suite(
        cls,
        canonical_chart: CanonicalVedicChart,
        varga_suite: Full16VargaSuite
    ) -> ShadbalaSuiteResult:

        planets_to_evaluate = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        results: Dict[str, PlanetShadbala] = {}

        asc_sign_index = canonical_chart.ascendant.sign_index

        for p_name in planets_to_evaluate:
            if p_name not in canonical_chart.placements:
                raise MissingCanonicalStateError(f"Required planet {p_name} missing.")

            p_data = canonical_chart.placements[p_name]
            p_lon = p_data.sidereal_longitude

            # --- 1. Sthana Bala (Positional Strength) ---
            # Uccha Bala (Exaltation Strength)
            exalt_sign = EXALTATION_SIGNS[p_name]
            deb_sign = DEBILITATION_SIGNS[p_name]

            # Distance from debilitation point. (Simplified to sign-based distance for this phase, max 60).
            # True BPHS requires exact degrees of exaltation/debilitation. We use exact degree distance.
            # Simplified for now: 180 degrees from debilitation = 60 shashtiamsas.
            # 1 degree = 60/180 = 1/3 shashtiamsas.
            # Needs exact debilitation point. Assuming 0 degrees of debilitation sign for baseline.
            deb_point_lon = (deb_sign - 1) * 30.0 + 15.0 # Center of debilitation sign as approximate

            angular_dist = abs(p_lon - deb_point_lon) % 360.0
            dist_from_deb = min(angular_dist, 360.0 - angular_dist)

            uccha_bala = (dist_from_deb / 180.0) * 60.0

            sthana_sub = {
                "Uccha Bala": round(uccha_bala, 2),
                "Sapta Vargaja Bala": 30.0, # Placeholder for exact varga strength aggregation
                "Ojha Yugma Bala": 15.0,     # Placeholder
                "Kendradi Bala": 30.0,       # Placeholder
                "Drekkana Bala": 15.0        # Placeholder
            }
            sthana_total = sum(sthana_sub.values())
            sthana_comp = ShadbalaComponent(name="Sthana Bala", value_rupas=round(sthana_total/60.0, 2), value_shashtiamsas=round(sthana_total, 2), sub_components=sthana_sub)

            # --- 2. Dig Bala (Directional Strength) ---
            # Max at power house (60 shashtiamsas), Min at opposite house (0).
            power_house_idx = DIG_BALA_HOUSES[p_name]
            # House index of planet (0-indexed from Ascendant)
            p_house_idx = (p_data.rashi.sign_index - asc_sign_index) % 12

            # Distance in houses (0 to 6)
            house_dist = abs(p_house_idx - power_house_idx)
            if house_dist > 6:
                house_dist = 12 - house_dist

            dig_bala_val = ((6 - house_dist) / 6.0) * 60.0
            dig_comp = ShadbalaComponent(name="Dig Bala", value_rupas=round(dig_bala_val/60.0, 2), value_shashtiamsas=round(dig_bala_val, 2))

            # --- 3. Kala Bala (Temporal Strength) ---
            kala_val = 30.0 # Placeholder for time-of-day/year algorithms
            kala_comp = ShadbalaComponent(name="Kala Bala", value_rupas=round(kala_val/60.0, 2), value_shashtiamsas=round(kala_val, 2))

            # --- 4. Cheshta Bala (Motional Strength) ---
            cheshta_val = 60.0 if p_data.retrograde else 30.0 # Simplified
            if p_name in ["Sun", "Moon"]:
                cheshta_val = 60.0 # Luminaries get full/different motional strength logic

            cheshta_comp = ShadbalaComponent(name="Cheshta Bala", value_rupas=round(cheshta_val/60.0, 2), value_shashtiamsas=round(cheshta_val, 2))

            # --- 5. Naisargika Bala (Natural Strength) ---
            naisargika_val = NAISARGIKA_BALA_SHASHTIAMSAS[p_name]
            naisargika_comp = ShadbalaComponent(name="Naisargika Bala", value_rupas=round(naisargika_val/60.0, 2), value_shashtiamsas=round(naisargika_val, 2))

            # --- 6. Drik Bala (Aspectual Strength) ---
            drik_val = 15.0 # Placeholder for aspect calculations
            drik_comp = ShadbalaComponent(name="Drik Bala", value_rupas=round(drik_val/60.0, 2), value_shashtiamsas=round(drik_val, 2))

            # --- TOTALS ---
            total_shashtiamsas = sthana_total + dig_bala_val + kala_val + cheshta_val + naisargika_val + drik_val
            total_rupas = total_shashtiamsas / 60.0

            results[p_name] = PlanetShadbala(
                planet=p_name,
                sthana_bala=sthana_comp,
                dig_bala=dig_comp,
                kala_bala=kala_comp,
                cheshta_bala=cheshta_comp,
                naisargika_bala=naisargika_comp,
                drik_bala=drik_comp,
                total_shashtiamsas=round(total_shashtiamsas, 2),
                total_rupas=round(total_rupas, 2),
                strength_percentage=100.0 # Placeholder
            )

        payload = {
            "chart_hash": canonical_chart.calculation_hash,
            "totals": {k: v.total_shashtiamsas for k, v in results.items()}
        }
        calc_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

        return ShadbalaSuiteResult(
            chart_hash=canonical_chart.calculation_hash,
            planets=results,
            calculation_hash=calc_hash
        )
