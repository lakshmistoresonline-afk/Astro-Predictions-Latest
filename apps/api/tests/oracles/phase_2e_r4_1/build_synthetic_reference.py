"""
Generate 5 Synthetic Boundary Reference Datasets for Phase 2E-R4.1.
Zero production engine imports!
"""
import json
import os
from pathlib import Path

ref_dir = Path(__file__).parent.parent.parent.parent / "fixtures" / "phase_2e_r4_1_reference"
ref_dir.mkdir(parents=True, exist_ok=True)

synthetics = [
    ("REF_016", "Sun Exaltation Boundary", 0.0, {"Sun": {"lon": 10.0}, "Moon": {"lon": 0.0}, "Mars": {"lon": 0.0}, "Mercury": {"lon": 0.0}, "Jupiter": {"lon": 0.0}, "Venus": {"lon": 0.0}, "Saturn": {"lon": 0.0}}),
    ("REF_017", "Sun Debilitation Boundary", 0.0, {"Sun": {"lon": 190.0}, "Moon": {"lon": 0.0}, "Mars": {"lon": 0.0}, "Mercury": {"lon": 0.0}, "Jupiter": {"lon": 0.0}, "Venus": {"lon": 0.0}, "Saturn": {"lon": 0.0}}),
    ("REF_018", "Cardinal Dig Bala Power", 0.0, {"Sun": {"lon": 270.0}, "Mars": {"lon": 270.0}, "Moon": {"lon": 180.0}, "Mercury": {"lon": 0.0}, "Jupiter": {"lon": 0.0}, "Venus": {"lon": 180.0}, "Saturn": {"lon": 180.0}}),
    ("REF_019", "Cardinal Dig Bala Zero", 0.0, {"Sun": {"lon": 90.0}, "Mars": {"lon": 90.0}, "Moon": {"lon": 270.0}, "Mercury": {"lon": 180.0}, "Jupiter": {"lon": 180.0}, "Venus": {"lon": 270.0}, "Saturn": {"lon": 0.0}}),
    ("REF_020", "High Speed Velocity", 0.0, {"Sun": {"lon": 0.0}, "Moon": {"lon": 0.0}, "Mars": {"lon": 0.0, "vel": 1.5, "retro": False}, "Mercury": {"lon": 0.0, "vel": -0.5, "retro": True}, "Jupiter": {"lon": 0.0}, "Venus": {"lon": 0.0}, "Saturn": {"lon": 0.0}})
]

for fid, name, asc_lon, p_dict in synthetics:
    planets_data = {}
    for p_name in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        info = p_dict.get(p_name, {"lon": 0.0})
        lon = info["lon"]
        vel = info.get("vel", 1.0)
        retro = info.get("retro", False)
        planets_data[p_name] = {
            "longitude": round(lon, 6),
            "velocity_deg_day": round(vel, 6),
            "retrograde": retro
        }

    ref_doc = {
        "fixture_id": fid,
        "name": name,
        "local_year": 2000, "local_month": 1, "local_day": 1,
        "local_hour": 12, "local_minute": 0,
        "timezone_str": "UTC",
        "birth_datetime_utc": "2000-01-01T12:00:00Z",
        "julian_day": 2451545.0,
        "latitude": 0.0,
        "longitude": 0.0,
        "ascendant_sidereal_longitude": round(asc_lon, 6),
        "mc_sidereal_longitude": round((asc_lon - 90)%360, 6),
        "ayanamsha": 23.85,
        "planets": planets_data,
        "type": "SYNTHETIC_BOUNDARY",
        "provenance": "Synthetic Angular/Velocity Boundary Reference Dataset"
    }

    out_path = ref_dir / f"{fid}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(ref_doc, f, indent=2)

print("Generated 5 synthetic boundary reference datasets! Total reference files =", len(list(ref_dir.glob("*.json"))))
