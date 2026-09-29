"""
Standalone Ephemeris Reference Data Extractor (Phase 2E-R4.1-R2).
Computes raw astronomical reference JSON datasets using PyEphem 4.2.1 (XEphem Engine).
ABSOLUTELY ZERO IMPORTS FROM apps.api.engines.*!
"""
import datetime
import hashlib
import json
import math
import os
from pathlib import Path

import ephem

# Pure Standalone Julian Day calculation (Meeus Ch. 7)
def calculate_standalone_julian_day(year: int, month: int, day: int, hour: float) -> float:
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100.0)
    B = 2 - A + math.floor(A / 4.0)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    return jd + (hour / 24.0)

# Pure Standalone Lahiri Ayanamsha (N.C. Lahiri Ephemeris)
def calculate_standalone_lahiri_ayanamsha(jd: float) -> float:
    T = (jd - 2451545.0) / 36525.0
    return 23.85 + 1.396 * T

# PyEphem Planet Mapping
EPHEM_PLANETS = {
    "Sun": ephem.Sun(),
    "Moon": ephem.Moon(),
    "Mars": ephem.Mars(),
    "Mercury": ephem.Mercury(),
    "Jupiter": ephem.Jupiter(),
    "Venus": ephem.Venus(),
    "Saturn": ephem.Saturn()
}

def extract_pyephem_positions(utc_datetime_iso: str, lat: float, lon: float, ayanamsha: float) -> dict:
    """Extracts raw sidereal longitudes and daily velocities using PyEphem (XEphem Engine)."""
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.elevation = 0
    observer.date = utc_datetime_iso.replace("T", " ").replace("Z", "")

    planets_out = {}
    for name, body in EPHEM_PLANETS.items():
        body.compute(observer)
        # Convert equatorial / ecliptic coordinates
        ecl = ephem.Ecliptic(body)
        trop_lon_deg = math.degrees(ecl.lon)
        sid_lon_deg = (trop_lon_deg - ayanamsha) % 360.0

        # Calculate velocity by sampling +1 hour
        observer_next = ephem.Observer()
        observer_next.lat = str(lat)
        observer_next.lon = str(lon)
        observer_next.date = ephem.Date(observer.date + ephem.hour)
        body_next = type(body)()
        body_next.compute(observer_next)
        ecl_next = ephem.Ecliptic(body_next)
        trop_next = math.degrees(ecl_next.lon)

        vel_deg_day = (trop_next - trop_lon_deg) * 24.0
        if vel_deg_day < -180: vel_deg_day += 360 * 24
        elif vel_deg_day > 180: vel_deg_day -= 360 * 24

        is_retro = vel_deg_day < 0.0

        planets_out[name] = {
            "longitude": round(sid_lon_deg, 6),
            "velocity_deg_day": round(vel_deg_day, 6),
            "retrograde": is_retro
        }

    return planets_out

# Standalone MC & Ascendant calculation (Meeus Ch. 14 / LST Geometry)
def calculate_standalone_ascendant_mc(jd: float, lat: float, lon: float, ayanamsha: float) -> tuple:
    T = (jd - 2451545.0) / 36525.0
    # Greenwich Mean Sidereal Time (GMST) in degrees
    gmst = (280.46061837 + 36000.770053608 * T + 0.000387933 * T**2) % 360.0
    # Local Sidereal Time (LST) in degrees
    lst = (gmst + lon) % 360.0

    # Tropical MC
    eps = 23.43929111 - 0.013004167 * T # Obliquity of ecliptic
    eps_rad = math.radians(eps)
    lst_rad = math.radians(lst)

    trop_mc = math.degrees(math.atan2(math.tan(lst_rad), math.cos(eps_rad))) % 360.0
    if lst > 180 and trop_mc < 180: trop_mc += 180
    elif lst < 180 and trop_mc > 180: trop_mc -= 180

    # Tropical Ascendant
    lat_rad = math.radians(lat)
    num = math.cos(lst_rad)
    den = -math.sin(lst_rad) * math.cos(eps_rad) - math.tan(lat_rad) * math.sin(eps_rad)
    trop_asc = math.degrees(math.atan2(num, den)) % 360.0

    sid_asc = (trop_asc - ayanamsha) % 360.0
    sid_mc = (trop_mc - ayanamsha) % 360.0

    return round(sid_asc, 6), round(sid_mc, 6)

REFERENCE_PROFILES_RAW = [
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

def run_extraction():
    raw_dir = Path(__file__).parent / "raw_reference"
    target_fixture_dir = Path(__file__).parent.parent.parent / "fixtures" / "phase_2e_r4_1_reference"

    raw_dir.mkdir(parents=True, exist_ok=True)
    target_fixture_dir.mkdir(parents=True, exist_ok=True)

    manifest_records = []

    for fid, name, y, m, d, h, mn, tz, lat, lon, utc_iso in REFERENCE_PROFILES_RAW:
        dt_parts = utc_iso.replace("Z", "").split("T")
        time_parts = [float(x) for x in dt_parts[1].split(":")]
        utc_hour = time_parts[0] + time_parts[1]/60.0 + time_parts[2]/360.0

        date_parts = [int(x) for x in dt_parts[0].split("-")]
        jd = calculate_standalone_julian_day(date_parts[0], date_parts[1], date_parts[2], utc_hour)
        ayanamsha = calculate_standalone_lahiri_ayanamsha(jd)

        # Extract planets using PyEphem 4.2.1
        planets_data = extract_pyephem_positions(utc_iso, lat, lon, ayanamsha)

        # Extract Ascendant and MC
        sid_asc, sid_mc = calculate_standalone_ascendant_mc(jd, lat, lon, ayanamsha)

        raw_doc = {
            "fixture_id": fid,
            "name": name,
            "source_engine": "PyEphem 4.2.1 (XEphem C Astronomical Ephemeris Core)",
            "license": "MIT License",
            "local_year": y, "local_month": m, "local_day": d,
            "local_hour": h, "local_minute": mn,
            "timezone_str": tz,
            "birth_datetime_utc": utc_iso,
            "julian_day": round(jd, 6),
            "latitude": lat,
            "longitude": lon,
            "ascendant_sidereal_longitude": sid_asc,
            "mc_sidereal_longitude": sid_mc,
            "ayanamsha": round(ayanamsha, 6),
            "planets": planets_data,
            "type": "REAL_REFERENCE"
        }

        doc_bytes = json.dumps(raw_doc, sort_keys=True).encode("utf-8")
        sha256_hash = hashlib.sha256(doc_bytes).hexdigest()
        raw_doc["sha256_manifest_hash"] = sha256_hash

        raw_path = raw_dir / f"{fid}.json"
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump(raw_doc, f, indent=2)

        target_path = target_fixture_dir / f"{fid}.json"
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(raw_doc, f, indent=2)

        manifest_records.append({
            "fixture_id": fid,
            "file": f"{fid}.json",
            "sha256": sha256_hash,
            "source": "PyEphem 4.2.1 (XEphem C Engine)"
        })

    manifest_path = Path(__file__).parent.parent.parent.parent.parent / "PHASE_2E_R4_1_REFERENCE_MANIFEST.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_records, f, indent=2)

    print(f"Extracted {len(manifest_records)} raw PyEphem 4.2.1 reference datasets! Written manifest to PHASE_2E_R4_1_REFERENCE_MANIFEST.json")

if __name__ == "__main__":
    run_extraction()
