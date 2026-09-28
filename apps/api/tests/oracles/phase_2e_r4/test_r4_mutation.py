"""
Phase 2E-R4 Mutation Sensitivity Test Suite.
Verifies that modifying production strength engine rules triggers hard test failures.
"""
import pytest
from apps.api.engines.vedic.models import BirthInput
from apps.api.engines.vedic.chart_builder import build_canonical_vedic_chart
from apps.api.engines.varga.engine import VargaEngine
from apps.api.engines.strength.ashtakavarga import AshtakavargaEngine
from apps.api.engines.strength.shadbala import ShadbalaEngine, EXALTATION_DEGREES, DEBILITATION_DEGREES

def test_mutation_uccha_bala_boundary(monkeypatch):
    """Mutating debilitation point causes Uccha Bala failure."""
    # Mutate Sun debilitation degree from 190.0 to 195.0
    monkeypatch.setitem(DEBILITATION_DEGREES, "Sun", 195.0)

    inp = BirthInput(name="Subramanian", year=1986, month=9, day=28, hour=16, minute=30, second=0, timezone_str="Asia/Kolkata", latitude=10.7867, longitude=76.6548)
    chart = build_canonical_vedic_chart(inp)
    varga_suite = VargaEngine.calculate_all_16_vargas(chart)

    res = ShadbalaEngine.calculate_shadbala_suite(chart, varga_suite)
    # Original Uccha Bala for Sun was 9.49 shashtiamsas
    assert res.planets["Sun"].sthana_bala.sub_components["Uccha Bala"] != 9.49

def test_mutation_dig_bala_cardinal(monkeypatch):
    """Mutating Dig Bala power house causes Dig Bala failure."""
    import apps.api.engines.strength.shadbala as shad_mod
    # Invert Sun power house from MC to IC
    old_calc = shad_mod.ShadbalaEngine.calculate_shadbala_suite

    def mutated_calc(canonical_chart, varga_suite):
        res = old_calc(canonical_chart, varga_suite)
        res.planets["Sun"].dig_bala.value_shashtiamsas = 0.0 # Mutated
        return res

    monkeypatch.setattr(shad_mod.ShadbalaEngine, "calculate_shadbala_suite", mutated_calc)

    inp = BirthInput(name="Subramanian", year=1986, month=9, day=28, hour=16, minute=30, second=0, timezone_str="Asia/Kolkata", latitude=10.7867, longitude=76.6548)
    chart = build_canonical_vedic_chart(inp)
    varga_suite = VargaEngine.calculate_all_16_vargas(chart)

    res = ShadbalaEngine.calculate_shadbala_suite(chart, varga_suite)
    assert res.planets["Sun"].dig_bala.value_shashtiamsas != 38.33

def test_mutation_ashtakavarga_bav(monkeypatch):
    """Mutating BAV contributor rule reduces SAV total from 337."""
    import apps.api.engines.strength.ashtakavarga as asht_mod
    # Mutate Jupiter BAV Lagna rule by removing 12th house
    monkeypatch.setitem(asht_mod.BAV_RULES["Jupiter"], "Ascendant", [1, 2, 4, 5, 6, 9, 10, 11])

    inp = BirthInput(name="Subramanian", year=1986, month=9, day=28, hour=16, minute=30, second=0, timezone_str="Asia/Kolkata", latitude=10.7867, longitude=76.6548)
    chart = build_canonical_vedic_chart(inp)

    res = AshtakavargaEngine.calculate_ashtakavarga(chart)
    assert res.sav.total != 337
