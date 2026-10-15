"""
Comprehensive Regression Test Suite for Planetary Placement Schema Integrity,
Astronomical Coordinate Fidelity, Rashi Sanskrit Names, and Nakshatra Lords.
"""
import pytest
from apps.api.engines.vedic.models import (
    BirthInput,
    RashiInfo,
    RashiPosition,
    NakshatraPadaInfo,
    PlanetaryVedicPlacement,
    HouseCuspInfo,
    CanonicalVedicChart
)
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.vedic.rashi import calculate_rashi, ZODIAC_SIGNS, RASHI_LORDS
from apps.api.engines.vedic.nakshatra import calculate_nakshatra_pada, NAKSHATRA_NAMES
from apps.api.engines.vedic.houses import generate_whole_sign_houses

def test_planetary_placement_coordinate_fidelity():
    """Verifies that geocentric latitude, distance, tropical longitude, and velocity survive without default substitution."""
    rashi = calculate_rashi(161.215) # Virgo
    nak_pada = calculate_nakshatra_pada(161.215) # Hasta

    placement = PlanetaryVedicPlacement(
        body_name="Venus",
        sidereal_longitude=161.215,
        geocentric_tropical_lon=184.886,
        geocentric_latitude=2.3514,
        distance_au=0.723,
        speed_deg_per_day=1.182,
        velocity_deg_day=1.182,
        retrograde=False,
        rashi=rashi,
        nakshatra_pada=nak_pada
    )

    assert placement.geocentric_latitude == 2.3514
    assert placement.distance_au == 0.723
    assert placement.speed_deg_per_day == 1.182
    assert placement.geocentric_tropical_lon == 184.886
    assert placement.sidereal_longitude != placement.geocentric_tropical_lon

def test_retrograde_negative_velocity_preserved():
    """Apparent retrograde motion with negative velocity must be preserved."""
    rashi = calculate_rashi(311.25)
    nak_pada = calculate_nakshatra_pada(311.25)

    retro_mars = PlanetaryVedicPlacement(
        body_name="Mars",
        sidereal_longitude=311.25,
        geocentric_tropical_lon=334.92,
        geocentric_latitude=-1.852,
        distance_au=0.612,
        speed_deg_per_day=-0.412,
        velocity_deg_day=-0.412,
        retrograde=True,
        rashi=rashi,
        nakshatra_pada=nak_pada
    )

    assert retro_mars.retrograde is True
    assert retro_mars.speed_deg_per_day == -0.412
    assert retro_mars.velocity_deg_day == -0.412

def test_rashi_sanskrit_names_derived_correctly():
    """All 12 Rashis must derive their exact Sanskrit names and lords."""
    sanskrit_ground_truth = [
        "Mesha", "Vrishabha", "Mithuna", "Karka",
        "Simha", "Kanya", "Tula", "Vrishchika",
        "Dhanu", "Makara", "Kumbha", "Meena"
    ]

    for sign_idx in range(1, 13):
        lon = (sign_idx - 1) * 30.0 + 15.0
        rashi_info = calculate_rashi(lon)
        assert rashi_info.sign_index == sign_idx
        assert rashi_info.sign == ZODIAC_SIGNS[sign_idx - 1]
        assert rashi_info.sanskrit_name == sanskrit_ground_truth[sign_idx - 1]

def test_nakshatra_ruling_planets_derived_correctly():
    """All 27 Nakshatras must derive their authoritative Vimshottari lord."""
    lord_ground_truth = [
        "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
        "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
        "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"
    ]

    for nak_num in range(1, 28):
        lon = (nak_num - 1) * (360.0 / 27.0) + 1.0
        nak_info = calculate_nakshatra_pada(lon)
        assert nak_info.nakshatra_number == nak_num
        assert nak_info.ruling_planet == lord_ground_truth[nak_num - 1]

def test_whole_sign_houses_derive_exact_lords_and_sanskrit_names():
    """Whole sign house generator must populate exact Sanskrit names and lords for all 12 houses."""
    asc_rashi = RashiPosition(
        sign_index=11, sign="Aquarius", sanskrit_name="Kumbha",
        degree=12, minute=40, second=0.0, absolute_longitude=312.666
    )

    houses = generate_whole_sign_houses(asc_rashi)
    assert len(houses) == 12

    # House 1 = Aquarius (Kumbha, Lord Saturn)
    assert houses[0].house_number == 1
    assert houses[0].sign_name == "Aquarius"
    assert houses[0].sanskrit_name == "Kumbha"
    assert houses[0].lord_planet == "Saturn"

    # House 2 = Pisces (Meena, Lord Jupiter)
    assert houses[1].house_number == 2
    assert houses[1].sign_name == "Pisces"
    assert houses[1].sanskrit_name == "Meena"
    assert houses[1].lord_planet == "Jupiter"

    # House 10 = Scorpio (Vrishchika, Lord Mars)
    assert houses[9].house_number == 10
    assert houses[9].sign_name == "Scorpio"
    assert houses[9].sanskrit_name == "Vrishchika"
    assert houses[9].lord_planet == "Mars"

def test_chart_construction_preserves_ayanamsha_and_metadata():
    """Chart construction must preserve calculated ayanamsha value and ephemeris metadata."""
    inp = BirthInput(
        name="Subramanian T S",
        year=1986, month=9, day=28,
        hour=16, minute=30, second=0,
        timezone_str="Asia/Kolkata",
        latitude=10.7867, longitude=76.6548
    )

    chart = build_canonical_vedic_chart(inp)
    assert chart.ayanamsha_mode == "Lahiri"
    assert 23.6 <= chart.ayanamsha_value_deg <= 23.8
    assert "ephemeris_kernel" in chart.metadata
    assert chart.ascendant.sign == "Aquarius"
    assert chart.mc.sign == "Scorpio"
