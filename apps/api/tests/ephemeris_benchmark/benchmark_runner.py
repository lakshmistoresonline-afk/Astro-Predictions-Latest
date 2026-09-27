"""
Benchmark runner for independent ephemeris accuracy assessment.
"""
import time
from apps.api.engines.birth_engine import BirthDataEngine
from apps.api.engines.astronomical_engine import AstronomicalEngine
from apps.api.tests.ephemeris_benchmark.reference_data import REFERENCE_CASES

class EphemerisBenchmarkRunner:

    @classmethod
    def run_benchmark(cls) -> dict:
        results = []
        start_time = time.time()

        for case in REFERENCE_CASES:
            # Parse dob
            parts = case["dob"].split("-")
            year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
            time_parts = case["time"].split(":")
            hour, minute = int(time_parts[0]), int(time_parts[1])

            birth_data = BirthDataEngine.process_birth_data(
                name=case["name"],
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                latitude=case["lat"],
                longitude=case["lon"],
                place_name=case["place"],
                country="India" if "India" in case["place"] or "Kerala" in case["place"] else "UK"
            )

            jd = birth_data["julian_day"]
            positions = AstronomicalEngine.calculate_positions(jd, case["lat"], case["lon"], "sidereal", "lahiri")

            results.append({
                "case_id": case["case_id"],
                "birth_data": birth_data,
                "positions": positions
            })

        duration = time.time() - start_time
        return {
            "execution_time_seconds": duration,
            "cases_tested": len(results),
            "results": results
        }
