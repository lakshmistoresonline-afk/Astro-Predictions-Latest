"""
Standalone PyEphem Reference Extractor (Phase 2E-R4.1-R4).
Reads input specifications from reference_source/inputs/ and calculates raw PyEphem 4.2.1 astronomical positions.
Zero imports from apps.api.engines.*!
"""
import datetime
import json
import math
import os
import platform
import sys
from pathlib import Path

import ephem

def calculate_standalone_julian_day(year: int, month: int, day: int, hour: float) -> float:
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100.0)
    B = 2 - A + math.floor(A / 4.0)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    return jd + (hour / 24.0)

def calculate_standalone_lahiri_ayanamsha(jd: float) -> float:
    T = (jd - 2451545.0) / 36525.0
    return 23.85 + 1.396 * T

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
    """Extracts raw tropical/sidereal longitudes, ecliptic latitudes, and daily velocities using PyEphem (XEphem Engine)."""
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.elevation = 0
    observer.date = utc_datetime_iso.replace("T", " ").replace("Z", "")

    planets_out = {}
    for name, body in EPHEM_PLANETS.items():
        body.compute(observer)
        ecl = ephem.Ecliptic(body)
        trop_lon_deg = math.degrees(ecl.lon)
        ecl_lat_deg = math.degrees(ecl.lat)
        sid_lon_deg = (trop_lon_deg - ayanamsha) % 360.0

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
            "tropical_longitude": round(trop_lon_deg, 6),
            "ecliptic_latitude": round(ecl_lat_deg, 6),
            "longitude": round(sid_lon_deg, 6),
            "velocity_deg_day": round(vel_deg_day, 6),
            "retrograde": is_retro
        }

    return planets_out

def calculate_standalone_ascendant_mc(utc_datetime_iso: str, lat: float, lon: float, ayanamsha: float, jd: float) -> tuple:
    observer = ephem.Observer()
    observer.lat = str(lat)
    observer.lon = str(lon)
    observer.elevation = 0
    observer.date = utc_datetime_iso.replace("T", " ").replace("Z", "")

    lst_rad = float(observer.sidereal_time())
    lst_deg = math.degrees(lst_rad)

    T = (jd - 2451545.0) / 36525.0
    eps = 23.43929111 - 0.013004167 * T
    eps_rad = math.radians(eps)

    # Tropical MC
    trop_mc = math.degrees(math.atan2(math.tan(lst_rad), math.cos(eps_rad))) % 360.0
    if 180.0 <= lst_deg < 360.0 and trop_mc < 180.0:
        trop_mc += 180.0
    elif 0.0 <= lst_deg < 180.0 and trop_mc >= 180.0:
        trop_mc -= 180.0

    # Tropical Ascendant
    lat_rad = math.radians(lat)
    num = math.cos(lst_rad)
    den = -math.sin(lst_rad) * math.cos(eps_rad) - math.tan(lat_rad) * math.sin(eps_rad)
    trop_asc = math.degrees(math.atan2(num, den)) % 360.0

    sid_asc = (trop_asc - ayanamsha) % 360.0
    sid_mc = (trop_mc - ayanamsha) % 360.0

    return round(sid_asc, 6), round(sid_mc, 6)

def run_pyephem_extraction():
    in_dir = Path(__file__).parent.parent / "inputs"
    out_dir = Path(__file__).parent

    in_files = sorted(list(in_dir.glob("*.json")))
    results = {}

    for in_file in in_files:
        with open(in_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        fid = data["fixture_id"]

        if data.get("type") == "SYNTHETIC_BOUNDARY":
            planets_data = data["synthetic_planets"]
            sid_asc = round(data["latitude"], 6)
            sid_mc = round((sid_asc - 90)%360, 6)
            jd = 2451545.0
            ayanamsha = 23.85
        else:
            dt_parts = data["birth_datetime_utc"].replace("Z", "").split("T")
            time_parts = [float(x) for x in dt_parts[1].split(":")]
            utc_hour = time_parts[0] + time_parts[1]/60.0 + time_parts[2]/360.0
            date_parts = [int(x) for x in dt_parts[0].split("-")]

            jd = calculate_standalone_julian_day(date_parts[0], date_parts[1], date_parts[2], utc_hour)
            ayanamsha = calculate_standalone_lahiri_ayanamsha(jd)
            planets_data = extract_pyephem_positions(data["birth_datetime_utc"], data["latitude"], data["longitude"], ayanamsha)
            sid_asc, sid_mc = calculate_standalone_ascendant_mc(data["birth_datetime_utc"], data["latitude"], data["longitude"], ayanamsha, jd)

        res_doc = {
            "fixture_id": fid,
            "source_engine": "PyEphem 4.2.1 (XEphem Engine)",
            "version": ephem.__version__,
            "julian_day": round(jd, 6),
            "ayanamsha": round(ayanamsha, 6),
            "ascendant_sidereal_longitude": sid_asc,
            "mc_sidereal_longitude": sid_mc,
            "planets": planets_data
        }

        results[fid] = res_doc

        with open(out_dir / f"{fid}.json", "w", encoding="utf-8") as f:
            json.dump(res_doc, f, indent=2)

    print(f"Extracted {len(results)} PyEphem reference fixtures in reference_source/pyephem_reference/!")

if __name__ == "__main__":
    run_pyephem_extraction()
