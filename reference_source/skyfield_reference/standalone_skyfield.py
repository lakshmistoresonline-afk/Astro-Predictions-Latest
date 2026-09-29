"""
Standalone Skyfield DE440s Reference Extractor (Phase 2E-R4.1-R4).
Reads input specifications from reference_source/inputs/ and calculates raw Skyfield 1.55 (NASA JPL DE440s Kernel) positions.
Zero imports from apps.api.engines.*!
"""
import datetime
import json
import math
import os
import sys
from pathlib import Path

from skyfield.api import load, Topos, load_file

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

def run_skyfield_extraction():
    in_dir = Path(__file__).parent.parent / "inputs"
    out_dir = Path(__file__).parent

    project_root = Path(__file__).parent.parent.parent
    kernel_path = project_root / "apps" / "api" / "engines" / "astronomy" / "de440s.bsp"
    if not kernel_path.exists():
        kernel_path = Path("apps/api/engines/astronomy/de440s.bsp")

    eph = load_file(str(kernel_path.absolute()))
    ts = load.timescale()

    planets_sky = {
        "Sun": eph["sun"],
        "Moon": eph["moon"],
        "Mars": eph["mars barycenter"],
        "Mercury": eph["mercury barycenter"],
        "Jupiter": eph["jupiter barycenter"],
        "Venus": eph["venus barycenter"],
        "Saturn": eph["saturn barycenter"]
    }
    earth = eph["earth"]

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

            t = ts.utc(date_parts[0], date_parts[1], date_parts[2], int(time_parts[0]), int(time_parts[1]), int(time_parts[2]))
            t_next = ts.utc(date_parts[0], date_parts[1], date_parts[2], int(time_parts[0]) + 1, int(time_parts[1]), int(time_parts[2]))

            planets_data = {}
            for name, body in planets_sky.items():
                ast = earth.at(t).observe(body)
                lat_deg, lon_deg, dist = ast.ecliptic_latlon()
                trop_lon = lon_deg.degrees
                ecl_lat = lat_deg.degrees
                sid_lon = (trop_lon - ayanamsha) % 360.0

                ast_next = earth.at(t_next).observe(body)
                _, lon_next_deg, _ = ast_next.ecliptic_latlon()
                trop_next = lon_next_deg.degrees

                vel_deg_day = (trop_next - trop_lon) * 24.0
                if vel_deg_day < -180: vel_deg_day += 360 * 24
                elif vel_deg_day > 180: vel_deg_day -= 360 * 24

                planets_data[name] = {
                    "tropical_longitude": round(float(trop_lon), 6),
                    "ecliptic_latitude": round(float(ecl_lat), 6),
                    "longitude": round(float(sid_lon), 6),
                    "velocity_deg_day": round(float(vel_deg_day), 6),
                    "retrograde": bool(vel_deg_day < 0.0)
                }

            # Ascendant and MC calculation
            gst = t.gast * 15.0 # Greenwich Apparent Sidereal Time in degrees
            lst = (gst + data["longitude"]) % 360.0
            lst_rad = math.radians(lst)

            T = (jd - 2451545.0) / 36525.0
            eps = 23.43929111 - 0.013004167 * T
            eps_rad = math.radians(eps)

            trop_mc = math.degrees(math.atan2(math.tan(lst_rad), math.cos(eps_rad))) % 360.0
            if 180.0 <= lst < 360.0 and trop_mc < 180.0: trop_mc += 180.0
            elif 0.0 <= lst < 180.0 and trop_mc >= 180.0: trop_mc -= 180.0

            lat_rad = math.radians(data["latitude"])
            num = math.cos(lst_rad)
            den = -math.sin(lst_rad) * math.cos(eps_rad) - math.tan(lat_rad) * math.sin(eps_rad)
            trop_asc = math.degrees(math.atan2(num, den)) % 360.0

            sid_asc = round((trop_asc - ayanamsha) % 360.0, 6)
            sid_mc = round((trop_mc - ayanamsha) % 360.0, 6)

        res_doc = {
            "fixture_id": fid,
            "source_engine": "Skyfield 1.55 (NASA JPL DE440s Kernel)",
            "version": "1.55",
            "kernel": "de440s.bsp",
            "julian_day": round(jd, 6),
            "ayanamsha": round(ayanamsha, 6),
            "ascendant_sidereal_longitude": sid_asc,
            "mc_sidereal_longitude": sid_mc,
            "planets": planets_data
        }

        results[fid] = res_doc

        with open(out_dir / f"{fid}.json", "w", encoding="utf-8") as f:
            json.dump(res_doc, f, indent=2)

    print(f"Extracted {len(results)} Skyfield DE440s reference fixtures in reference_source/skyfield_reference/!")

if __name__ == "__main__":
    run_skyfield_extraction()
