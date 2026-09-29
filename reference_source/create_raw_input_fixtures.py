"""
Create raw, immutable birth input specification JSON files in reference_source/inputs/
Zero imports from apps.api.engines.*!
"""
import json
import os
from pathlib import Path

INPUT_PROFILES = [
    ("REF_001", "Subramanian T S", 1986, 9, 28, 16, 30, "Asia/Kolkata", 10.7867, 76.6548, "1986-09-28T11:00:00Z"),
    ("REF_002", "User A Kochi", 1990, 1, 15, 8, 30, "Asia/Kolkata", 9.9312, 76.2673, "1990-01-15T03:00:00Z"),
    ("REF_003", "User B London", 1985, 7, 22, 18, 45, "Europe/London", 51.5074, -0.1278, "1985-07-22T17:45:00Z"),
    ("REF_004", "New York Native", 2000, 1, 1, 12, 0, "America/New_York", 40.7128, -74.0060, "2000-01-01T17:00:00Z"),
    ("REF_005", "Tokyo Native", 1995, 5, 5, 9, 0, "Asia/Tokyo", 35.6762, 139.6503, "1995-05-05T00:00:00Z"),
    ("REF_006", "Sydney Native", 1998, 11, 12, 15, 30, "Australia/Sydney", -33.8688, 151.2093, "1998-11-12T04:30:00Z"),
    ("REF_007", "Paris Native", 1975, 3, 21, 6, 0, "Europe/Paris", 48.8566, 2.3522, "1975-03-21T05:00:00Z"),
    ("REF_008", "Reykjavik Native", 1992, 6, 21, 23, 45, "Atlantic/Reykjavik", 64.1466, -21.9426, "1992-06-21T23:45:00Z"),
    ("SHADBALA_FIXTURE_009", "Singapore Native", 2010, 8, 9, 18, 0, "Asia/Singapore", 1.3521, 103.8198, "2010-08-09T10:00:00Z"),
    ("SHADBALA_FIXTURE_010", "Los Angeles Retrograde", 2020, 10, 15, 20, 0, "America/Los_Angeles", 34.0522, -118.2437, "2020-10-16T03:00:00Z"),
    ("REF_011", "Berlin Native", 1988, 12, 12, 10, 15, "Europe/Berlin", 52.5200, 13.4050, "1988-12-12T09:15:00Z"),
    ("REF_012", "Cairo Native", 1991, 4, 10, 14, 0, "Africa/Cairo", 30.0444, 31.2357, "1991-04-10T12:00:00Z"),
    ("REF_013", "Buenos Aires Native", 1982, 2, 28, 8, 0, "America/Argentina/Buenos_Aires", -34.6037, -58.3816, "1982-02-28T11:00:00Z"),
    ("REF_014", "Mumbai Native", 1994, 8, 15, 22, 30, "Asia/Kolkata", 19.0760, 72.8777, "1994-08-15T17:00:00Z"),
    ("REF_015", "Honolulu Native", 2005, 7, 4, 5, 30, "Pacific/Honolulu", 21.3069, -157.8583, "2005-07-04T15:30:00Z")
]

SYNTHETIC_PROFILES = [
    ("REF_016", "Sun Exaltation Boundary", 2000, 1, 1, 12, 0, "UTC", 0.0, 0.0, "2000-01-01T12:00:00Z", {"Sun": {"longitude": 10.0, "velocity_deg_day": 1.0, "retrograde": False}, "Moon": {"longitude": 0.0, "velocity_deg_day": 13.0, "retrograde": False}, "Mars": {"longitude": 0.0, "velocity_deg_day": 0.5, "retrograde": False}, "Mercury": {"longitude": 0.0, "velocity_deg_day": 1.0, "retrograde": False}, "Jupiter": {"longitude": 0.0, "velocity_deg_day": 0.1, "retrograde": False}, "Venus": {"longitude": 0.0, "velocity_deg_day": 1.0, "retrograde": False}, "Saturn": {"longitude": 0.0, "velocity_deg_day": 0.05, "retrograde": False}}),
    ("REF_017", "Sun Debilitation Boundary", 2000, 1, 1, 12, 0, "UTC", 0.0, 0.0, "2000-01-01T12:00:00Z", {"Sun": {"longitude": 190.0, "velocity_deg_day": 1.0, "retrograde": False}, "Moon": {"longitude": 0.0, "velocity_deg_day": 13.0, "retrograde": False}, "Mars": {"longitude": 0.0, "velocity_deg_day": 0.5, "retrograde": False}, "Mercury": {"longitude": 0.0, "velocity_deg_day": 1.0, "retrograde": False}, "Jupiter": {"longitude": 0.0, "velocity_deg_day": 0.1, "retrograde": False}, "Venus": {"longitude": 0.0, "velocity_deg_day": 1.0, "retrograde": False}, "Saturn": {"longitude": 0.0, "velocity_deg_day": 0.05, "retrograde": False}}),
    ("REF_018", "Cardinal Dig Bala Power", 2000, 1, 1, 12, 0, "UTC", 0.0, 0.0, "2000-01-01T12:00:00Z", {"Sun": {"longitude": 270.0, "velocity_deg_day": 1.0, "retrograde": False}, "Mars": {"longitude": 270.0, "velocity_deg_day": 0.5, "retrograde": False}, "Moon": {"longitude": 180.0, "velocity_deg_day": 13.0, "retrograde": False}, "Mercury": {"longitude": 0.0, "velocity_deg_day": 1.0, "retrograde": False}, "Jupiter": {"longitude": 0.0, "velocity_deg_day": 0.1, "retrograde": False}, "Venus": {"longitude": 180.0, "velocity_deg_day": 1.0, "retrograde": False}, "Saturn": {"longitude": 180.0, "velocity_deg_day": 0.05, "retrograde": False}}),
    ("REF_019", "Cardinal Dig Bala Zero", 2000, 1, 1, 12, 0, "UTC", 0.0, 0.0, "2000-01-01T12:00:00Z", {"Sun": {"longitude": 90.0, "velocity_deg_day": 1.0, "retrograde": False}, "Mars": {"longitude": 90.0, "velocity_deg_day": 0.5, "retrograde": False}, "Moon": {"longitude": 270.0, "velocity_deg_day": 13.0, "retrograde": False}, "Mercury": {"longitude": 180.0, "velocity_deg_day": 1.0, "retrograde": False}, "Jupiter": {"longitude": 180.0, "velocity_deg_day": 0.1, "retrograde": False}, "Venus": {"longitude": 270.0, "velocity_deg_day": 1.0, "retrograde": False}, "Saturn": {"longitude": 0.0, "velocity_deg_day": 0.05, "retrograde": False}}),
    ("REF_020", "High Speed Velocity", 2000, 1, 1, 12, 0, "UTC", 0.0, 0.0, "2000-01-01T12:00:00Z", {"Sun": {"longitude": 0.0, "velocity_deg_day": 1.0, "retrograde": False}, "Moon": {"longitude": 0.0, "velocity_deg_day": 13.0, "retrograde": False}, "Mars": {"longitude": 0.0, "velocity_deg_day": 1.5, "retrograde": False}, "Mercury": {"longitude": 0.0, "velocity_deg_day": -0.5, "retrograde": True}, "Jupiter": {"longitude": 0.0, "velocity_deg_day": 0.1, "retrograde": False}, "Venus": {"longitude": 0.0, "velocity_deg_day": 1.0, "retrograde": False}, "Saturn": {"longitude": 0.0, "velocity_deg_day": 0.05, "retrograde": False}})
]

out_dir = Path(__file__).parent / "inputs"
out_dir.mkdir(parents=True, exist_ok=True)

for fid, name, y, m, d, h, mn, tz, lat, lon, utc_iso in INPUT_PROFILES:
    doc = {
        "fixture_id": fid,
        "name": name,
        "local_year": y, "local_month": m, "local_day": d,
        "local_hour": h, "local_minute": mn,
        "timezone_str": tz,
        "birth_datetime_utc": utc_iso,
        "latitude": lat,
        "longitude": lon,
        "type": "REAL_BIRTH_PROFILE"
    }
    with open(out_dir / f"{fid}.json", "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)

for fid, name, y, m, d, h, mn, tz, lat, lon, utc_iso, p_dict in SYNTHETIC_PROFILES:
    doc = {
        "fixture_id": fid,
        "name": name,
        "local_year": y, "local_month": m, "local_day": d,
        "local_hour": h, "local_minute": mn,
        "timezone_str": tz,
        "birth_datetime_utc": utc_iso,
        "latitude": lat,
        "longitude": lon,
        "type": "SYNTHETIC_BOUNDARY",
        "synthetic_planets": p_dict
    }
    with open(out_dir / f"{fid}.json", "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)

print("Successfully created 20 raw input specification JSONs in reference_source/inputs/!")
