"""
Comprehensive Unit & Forensic Verification Suite for Astrovision Astronomy Provider (Phase 1D-R).
Includes date boundary testing and fail-closed verification.
"""
import pytest
import os
from apps.api.engines.astronomy.exceptions import (
    KernelNotFoundError,
    ProviderInitializationError,
    CalculationError
)
from apps.api.engines.astronomy.providers.skyfield_jpl import SkyfieldJPLProvider


def test_provider_initialization_and_kernel_identity():
    """Verify provider initialization and exact kernel identity."""
    provider = SkyfieldJPLProvider()
    assert provider.kernel_filename in ["de440s.bsp", "de421.bsp"]
    assert len(provider.kernel_checksum) == 64 # SHA256 length


def test_fail_closed_behavior_on_missing_kernel():
    """Verify strict fail-closed behavior when non-existent kernel path is supplied. No silent fallback."""
    with pytest.raises(KernelNotFoundError):
        SkyfieldJPLProvider(kernel_path="non_existent_kernel_9999.bsp")


def test_canonical_subramanian_t_s_case():
    """Verify calculation result using the canonical Subramanian T S birth chart."""
    provider = SkyfieldJPLProvider()
    res = provider.calculate_astronomical_state(
        year=1986, month=9, day=28,
        hour=11, minute=0, second=0,
        lat=10.7867, lon=76.6548, elevation=0.0
    )

    # 1. Metadata completeness
    assert res.metadata.provider in ["SkyfieldJPLProvider", "Skyfield"]
    assert res.metadata.ephemeris_kernel in ["de440s.bsp", "de421.bsp"]
    assert len(res.metadata.calculation_hash) == 64 # SHA-256 length

    # 2. Raw Ephemeris Data
    raw = res.raw_ephemeris
    assert "Sun" in raw.bodies
    assert "Moon" in raw.bodies
    assert raw.bodies["Sun"].geocentric_longitude > 0
    assert raw.bodies["Moon"].geocentric_longitude > 0

    # 3. Derived Astronomical State
    derived = res.derived_astronomy
    assert 0 <= derived.ascendant_tropical_deg < 360
    assert 0 <= derived.mc_tropical_deg < 360

    # 4. Sidereal State (Lahiri)
    sid = res.sidereal_state
    assert sid.ayanamsha_mode == "Lahiri"
    assert 23.5 < sid.ayanamsha_value_deg < 24.5
    assert "Sun" in sid.sidereal_longitudes


def test_repeated_calculation_equality():
    """Verify strict determinism for identical inputs."""
    provider = SkyfieldJPLProvider()

    res1 = provider.calculate_astronomical_state(1986, 9, 28, 11, 0, 0, 10.7867, 76.6548)
    res2 = provider.calculate_astronomical_state(1986, 9, 28, 11, 0, 0, 10.7867, 76.6548)

    assert res1.metadata.calculation_hash == res2.metadata.calculation_hash
    assert res1.sidereal_state.sidereal_longitudes["Sun"] == res2.sidereal_state.sidereal_longitudes["Sun"]
    assert res1.sidereal_state.ascendant_sidereal_deg == res2.sidereal_state.ascendant_sidereal_deg


def test_time_sensitivity():
    """Verify sensitivity to birth time variation (1 hour shift)."""
    provider = SkyfieldJPLProvider()

    res_t1 = provider.calculate_astronomical_state(1986, 9, 28, 11, 0, 0, 10.7867, 76.6548)
    res_t2 = provider.calculate_astronomical_state(1986, 9, 28, 12, 0, 0, 10.7867, 76.6548)

    assert res_t1.raw_ephemeris.bodies["Moon"].geocentric_longitude != res_t2.raw_ephemeris.bodies["Moon"].geocentric_longitude
    assert res_t1.derived_astronomy.ascendant_tropical_deg != res_t2.derived_astronomy.ascendant_tropical_deg
    assert res_t1.metadata.calculation_hash != res_t2.metadata.calculation_hash


def test_observer_coordinate_sensitivity():
    """Verify sensitivity to geographic coordinate changes."""
    provider = SkyfieldJPLProvider()

    res_loc1 = provider.calculate_astronomical_state(1986, 9, 28, 11, 0, 0, 10.7867, 76.6548) # Palakkad
    res_loc2 = provider.calculate_astronomical_state(1986, 9, 28, 11, 0, 0, 51.5074, -0.1278) # London

    assert res_loc1.derived_astronomy.ascendant_tropical_deg != res_loc2.derived_astronomy.ascendant_tropical_deg
    assert res_loc1.metadata.calculation_hash != res_loc2.metadata.calculation_hash


def test_personalization_user_a_kochi_vs_user_b_london():
    """
    Verify Personalization:
    User A: 1990-01-15, Kochi (03:00 UTC, 9.9312 N, 76.2673 E)
    User B: 1985-07-22, London (17:45 UTC, 51.5074 N, -0.1278 E)
    """
    provider = SkyfieldJPLProvider()

    user_a = provider.calculate_astronomical_state(1990, 1, 15, 3, 0, 0, 9.9312, 76.2673)
    user_b = provider.calculate_astronomical_state(1985, 7, 22, 17, 45, 0, 51.5074, -0.1278)

    assert user_a.sidereal_state.sidereal_longitudes["Sun"] != user_b.sidereal_state.sidereal_longitudes["Sun"]
    assert user_a.sidereal_state.sidereal_longitudes["Moon"] != user_b.sidereal_state.sidereal_longitudes["Moon"]
    assert user_a.sidereal_state.ascendant_sidereal_deg != user_b.sidereal_state.ascendant_sidereal_deg
    assert user_a.metadata.calculation_hash != user_b.metadata.calculation_hash


def test_retrograde_state_velocity_derivation():
    """Verify that retrograde flag is strictly boolean and tied to negative longitudinal velocity."""
    provider = SkyfieldJPLProvider()
    res = provider.calculate_astronomical_state(1986, 9, 28, 11, 0, 0, 10.7867, 76.6548)

    for body_name, pos in res.raw_ephemeris.bodies.items():
        assert isinstance(pos.retrograde, bool)
        if pos.velocity_lon_deg_day < 0:
            assert pos.retrograde is True
        else:
            assert pos.retrograde is False


def test_boundary_dates_and_out_of_range_fail_closed():
    """
    Verify boundary date handling:
    1. Dates within loaded kernel boundary calculate correctly.
    2. Dates outside loaded kernel boundary raise CalculationError (fail closed).
    """
    provider = SkyfieldJPLProvider()

    # Valid date within kernel coverage
    res_valid = provider.calculate_astronomical_state(2026, 9, 27, 12, 0, 0, 40.7128, -74.0060)
    assert res_valid.raw_ephemeris.bodies["Sun"].geocentric_longitude > 0

    # Date far outside DE421/DE440s range (e.g. Year 1500)
    with pytest.raises(CalculationError):
        provider.calculate_astronomical_state(1500, 1, 1, 12, 0, 0, 10.7867, 76.6548)
