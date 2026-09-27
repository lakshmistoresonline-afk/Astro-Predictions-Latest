import pytest
from apps.api.tests.ephemeris_benchmark.benchmark_runner import EphemerisBenchmarkRunner

def test_ephemeris_benchmark_execution():
    report = EphemerisBenchmarkRunner.run_benchmark()
    assert report["cases_tested"] == 4
    assert report["execution_time_seconds"] < 5.0
    for res in report["results"]:
        assert "positions" in res
        assert "Sun" in res["positions"]
        assert "Moon" in res["positions"]
        assert "Rahu" in res["positions"]
        assert "Ketu" in res["positions"]
