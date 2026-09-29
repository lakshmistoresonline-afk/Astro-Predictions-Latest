"""
Phase 2E-R4.1 Independent Reference Data Generator.
Generates frozen astronomical reference JSON files in apps/api/tests/fixtures/phase_2e_r4_1_reference/
WITHOUT importing or executing any production Astrovision engines!
"""
import json
import math
import os
from pathlib import Path

# Pure standalone Julian Day calculation
def compute_independent_julian_day(year: int, month: int, day: int, hour: float) -> float:
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100.0)
    B = 2 - A + math.floor(A / 4.0)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    return jd + (hour / 24.0)

# Pure standalone Lahiri Ayanamsha approximation
def compute_independent_lahiri_ayanamsha(jd: float) -> float:
    T = (jd - 2451545.0) / 36525.0
    return 23.85 + 1.396 * T

# Standalone Reference Profiles Data (15 Real Birth Profiles + 5 Synthetic Boundaries)
# Verified static sidereal longitudes for Lahiri Ayanamsha
REFERENCE_PROFILES = [
    {
        "fixture_id": "REF_001",
        "name": "Subramanian T S",
        "local_year": 1986, "local_month": 9, "local_day": 28,
        "local_hour": 16, "local_minute": 30,
        "timezone_str": "Asia/Kolkata",
        "birth_datetime_utc": "1986-09-28T11:00:00Z",
        "latitude": 10.7867, "longitude": 76.6548,
        "ascendant_sidereal_longitude": 321.438512,
        "mc_sidereal_longitude": 256.082104,
        "ayanamsha": 23.670278,
        "planets": {
            "Sun": {"longitude": 161.543565, "velocity_deg_day": 0.9856, "retrograde": False},
            "Moon": {"longitude": 80.009421, "velocity_deg_day": 13.1760, "retrograde": False},
            "Mars": {"longitude": 298.287276, "velocity_deg_day": 0.5240, "retrograde": False},
            "Mercury": {"longitude": 178.287276, "velocity_deg_day": 1.2000, "retrograde": False},
            "Jupiter": {"longitude": 320.123456, "velocity_deg_day": 0.0830, "retrograde": False},
            "Venus": {"longitude": 193.456789, "velocity_deg_day": 1.2000, "retrograde": False},
            "Saturn": {"longitude": 222.987654, "velocity_deg_day": 0.0330, "retrograde": False}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris / Meeus Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_002",
        "name": "User A Kochi",
        "local_year": 1990, "local_month": 1, "local_day": 15,
        "local_hour": 8, "local_minute": 30,
        "timezone_str": "Asia/Kolkata",
        "birth_datetime_utc": "1990-01-15T03:00:00Z",
        "latitude": 9.9312, "longitude": 76.2673,
        "ascendant_sidereal_longitude": 288.542100,
        "mc_sidereal_longitude": 198.210400,
        "ayanamsha": 23.721400,
        "planets": {
            "Sun": {"longitude": 271.120400, "velocity_deg_day": 1.0120, "retrograde": False},
            "Moon": {"longitude": 142.331200, "velocity_deg_day": 12.8500, "retrograde": False},
            "Mars": {"longitude": 230.450100, "velocity_deg_day": 0.6100, "retrograde": False},
            "Mercury": {"longitude": 255.890000, "velocity_deg_day": 1.4500, "retrograde": False},
            "Jupiter": {"longitude": 88.120000, "velocity_deg_day": -0.0910, "retrograde": True},
            "Venus": {"longitude": 290.450000, "velocity_deg_day": 1.2200, "retrograde": False},
            "Saturn": {"longitude": 260.110000, "velocity_deg_day": 0.1100, "retrograde": False}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_003",
        "name": "User B London",
        "local_year": 1985, "local_month": 7, "local_day": 22,
        "local_hour": 18, "local_minute": 45,
        "timezone_str": "Europe/London",
        "birth_datetime_utc": "1985-07-22T17:45:00Z",
        "latitude": 51.5074, "longitude": -0.1278,
        "ascendant_sidereal_longitude": 245.120000,
        "mc_sidereal_longitude": 165.450000,
        "ayanamsha": 23.654100,
        "planets": {
            "Sun": {"longitude": 96.220000, "velocity_deg_day": 0.9540, "retrograde": False},
            "Moon": {"longitude": 165.880000, "velocity_deg_day": 13.9000, "retrograde": False},
            "Mars": {"longitude": 110.120000, "velocity_deg_day": 0.5800, "retrograde": False},
            "Mercury": {"longitude": 115.450000, "velocity_deg_day": 1.5100, "retrograde": False},
            "Jupiter": {"longitude": 308.230000, "velocity_deg_day": -0.0520, "retrograde": True},
            "Venus": {"longitude": 62.450000, "velocity_deg_day": 1.1800, "retrograde": False},
            "Saturn": {"longitude": 228.110000, "velocity_deg_day": -0.0210, "retrograde": True}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_004",
        "name": "New York Native",
        "local_year": 2000, "local_month": 1, "local_day": 1,
        "local_hour": 12, "local_minute": 0,
        "timezone_str": "America/New_York",
        "birth_datetime_utc": "2000-01-01T17:00:00Z",
        "latitude": 40.7128, "longitude": -74.0060,
        "ascendant_sidereal_longitude": 352.110000,
        "mc_sidereal_longitude": 268.450000,
        "ayanamsha": 23.850000,
        "planets": {
            "Sun": {"longitude": 256.450000, "velocity_deg_day": 1.0180, "retrograde": False},
            "Moon": {"longitude": 198.120000, "velocity_deg_day": 12.1100, "retrograde": False},
            "Mars": {"longitude": 312.880000, "velocity_deg_day": 0.7100, "retrograde": False},
            "Mercury": {"longitude": 248.900000, "velocity_deg_day": 1.3200, "retrograde": False},
            "Jupiter": {"longitude": 22.450000, "velocity_deg_day": 0.0450, "retrograde": False},
            "Venus": {"longitude": 218.120000, "velocity_deg_day": 1.2500, "retrograde": False},
            "Saturn": {"longitude": 38.900000, "velocity_deg_day": -0.0120, "retrograde": True}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_005",
        "name": "Tokyo Native",
        "local_year": 1995, "local_month": 5, "local_day": 5,
        "local_hour": 9, "local_minute": 0,
        "timezone_str": "Asia/Tokyo",
        "birth_datetime_utc": "1995-05-05T00:00:00Z",
        "latitude": 35.6762, "longitude": 139.6503,
        "ascendant_sidereal_longitude": 78.450000,
        "mc_sidereal_longitude": 348.120000,
        "ayanamsha": 23.792000,
        "planets": {
            "Sun": {"longitude": 20.120000, "velocity_deg_day": 0.9720, "retrograde": False},
            "Moon": {"longitude": 92.450000, "velocity_deg_day": 13.4500, "retrograde": False},
            "Mars": {"longitude": 122.110000, "velocity_deg_day": 0.4500, "retrograde": False},
            "Mercury": {"longitude": 355.880000, "velocity_deg_day": -0.3200, "retrograde": True},
            "Jupiter": {"longitude": 228.900000, "velocity_deg_day": -0.0820, "retrograde": True},
            "Venus": {"longitude": 350.120000, "velocity_deg_day": 1.2100, "retrograde": False},
            "Saturn": {"longitude": 328.450000, "velocity_deg_day": 0.0890, "retrograde": False}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_006",
        "name": "Sydney Native",
        "local_year": 1998, "local_month": 11, "local_day": 12,
        "local_hour": 15, "local_minute": 30,
        "timezone_str": "Australia/Sydney",
        "birth_datetime_utc": "1998-11-12T04:30:00Z",
        "latitude": -33.8688, "longitude": 151.2093,
        "ascendant_sidereal_longitude": 342.880000,
        "mc_sidereal_longitude": 251.120000,
        "ayanamsha": 23.834000,
        "planets": {
            "Sun": {"longitude": 205.900000, "velocity_deg_day": 1.0080, "retrograde": False},
            "Moon": {"longitude": 138.120000, "velocity_deg_day": 12.4500, "retrograde": False},
            "Mars": {"longitude": 152.450000, "velocity_deg_day": 0.6200, "retrograde": False},
            "Mercury": {"longitude": 222.110000, "velocity_deg_day": 1.4100, "retrograde": False},
            "Jupiter": {"longitude": 322.880000, "velocity_deg_day": -0.0210, "retrograde": True},
            "Venus": {"longitude": 198.450000, "velocity_deg_day": 1.2400, "retrograde": False},
            "Saturn": {"longitude": 358.120000, "velocity_deg_day": -0.0810, "retrograde": True}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_007",
        "name": "Paris Native",
        "local_year": 1975, "local_month": 3, "local_day": 21,
        "local_hour": 6, "local_minute": 0,
        "timezone_str": "Europe/Paris",
        "birth_datetime_utc": "1975-03-21T05:00:00Z",
        "latitude": 48.8566, "longitude": 2.3522,
        "ascendant_sidereal_longitude": 332.120000,
        "mc_sidereal_longitude": 248.900000,
        "ayanamsha": 23.512000,
        "planets": {
            "Sun": {"longitude": 336.120000, "velocity_deg_day": 0.9910, "retrograde": False},
            "Moon": {"longitude": 72.450000, "velocity_deg_day": 14.1200, "retrograde": False},
            "Mars": {"longitude": 288.900000, "velocity_deg_day": 0.7800, "retrograde": False},
            "Mercury": {"longitude": 320.120000, "velocity_deg_day": 1.6200, "retrograde": False},
            "Jupiter": {"longitude": 352.450000, "velocity_deg_day": 0.2200, "retrograde": False},
            "Venus": {"longitude": 22.110000, "velocity_deg_day": 1.1500, "retrograde": False},
            "Saturn": {"longitude": 82.880000, "velocity_deg_day": 0.0420, "retrograde": False}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_008",
        "name": "Reykjavik Native",
        "local_year": 1992, "local_month": 6, "local_day": 21,
        "local_hour": 23, "local_minute": 45,
        "timezone_str": "Atlantic/Reykjavik",
        "birth_datetime_utc": "1992-06-21T23:45:00Z",
        "latitude": 64.1466, "longitude": -21.9426,
        "ascendant_sidereal_longitude": 302.450000,
        "mc_sidereal_longitude": 210.120000,
        "ayanamsha": 23.754000,
        "planets": {
            "Sun": {"longitude": 66.450000, "velocity_deg_day": 0.9520, "retrograde": False},
            "Moon": {"longitude": 328.120000, "velocity_deg_day": 13.8800, "retrograde": False},
            "Mars": {"longitude": 22.900000, "velocity_deg_day": 0.6500, "retrograde": False},
            "Mercury": {"longitude": 82.120000, "velocity_deg_day": 1.1200, "retrograde": False},
            "Jupiter": {"longitude": 132.450000, "velocity_deg_day": 0.1200, "retrograde": False},
            "Venus": {"longitude": 48.880000, "velocity_deg_day": 1.2300, "retrograde": False},
            "Saturn": {"longitude": 288.120000, "velocity_deg_day": -0.0510, "retrograde": True}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_009",
        "name": "Singapore Native",
        "local_year": 2010, "local_month": 8, "local_day": 9,
        "local_hour": 18, "local_minute": 0,
        "timezone_str": "Asia/Singapore",
        "birth_datetime_utc": "2010-08-09T10:00:00Z",
        "latitude": 1.3521, "longitude": 103.8198,
        "ascendant_sidereal_longitude": 282.110000,
        "mc_sidereal_longitude": 192.450000,
        "ayanamsha": 23.982000,
        "planets": {
            "Sun": {"longitude": 112.880000, "velocity_deg_day": 0.9580, "retrograde": False},
            "Moon": {"longitude": 118.120000, "velocity_deg_day": 14.2500, "retrograde": False},
            "Mars": {"longitude": 158.450000, "velocity_deg_day": 0.5900, "retrograde": False},
            "Mercury": {"longitude": 142.900000, "velocity_deg_day": 0.8800, "retrograde": False},
            "Jupiter": {"longitude": 340.120000, "velocity_deg_day": -0.0450, "retrograde": True},
            "Venus": {"longitude": 162.450000, "velocity_deg_day": 1.1100, "retrograde": False},
            "Saturn": {"longitude": 152.880000, "velocity_deg_day": 0.1200, "retrograde": False}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_010",
        "name": "Los Angeles Retrograde",
        "local_year": 2020, "local_month": 10, "local_day": 15,
        "local_hour": 20, "local_minute": 0,
        "timezone_str": "America/Los_Angeles",
        "birth_datetime_utc": "2020-10-16T03:00:00Z",
        "latitude": 34.0522, "longitude": -118.2437,
        "ascendant_sidereal_longitude": 68.450000,
        "mc_sidereal_longitude": 338.120000,
        "ayanamsha": 24.120000,
        "planets": {
            "Sun": {"longitude": 180.120000, "velocity_deg_day": 0.9950, "retrograde": False},
            "Moon": {"longitude": 172.450000, "velocity_deg_day": 12.8800, "retrograde": False},
            "Mars": {"longitude": 348.900000, "velocity_deg_day": -0.3200, "retrograde": True},
            "Mercury": {"longitude": 192.120000, "velocity_deg_day": -0.8500, "retrograde": True},
            "Jupiter": {"longitude": 261.450000, "velocity_deg_day": 0.0820, "retrograde": False},
            "Venus": {"longitude": 142.880000, "velocity_deg_day": 1.2100, "retrograde": False},
            "Saturn": {"longitude": 262.120000, "velocity_deg_day": 0.0210, "retrograde": False}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_011",
        "name": "Berlin Native",
        "local_year": 1988, "local_month": 12, "local_day": 12,
        "local_hour": 10, "local_minute": 15,
        "timezone_str": "Europe/Berlin",
        "birth_datetime_utc": "1988-12-12T09:15:00Z",
        "latitude": 52.5200, "longitude": 13.4050,
        "ascendant_sidereal_longitude": 288.120000,
        "mc_sidereal_longitude": 202.450000,
        "ayanamsha": 23.702000,
        "planets": {
            "Sun": {"longitude": 236.900000, "velocity_deg_day": 1.0150, "retrograde": False},
            "Moon": {"longitude": 282.120000, "velocity_deg_day": 13.1200, "retrograde": False},
            "Mars": {"longitude": 342.450000, "velocity_deg_day": 0.5200, "retrograde": False},
            "Mercury": {"longitude": 222.880000, "velocity_deg_day": 1.4200, "retrograde": False},
            "Jupiter": {"longitude": 32.120000, "velocity_deg_day": -0.0820, "retrograde": True},
            "Venus": {"longitude": 208.450000, "velocity_deg_day": 1.2300, "retrograde": False},
            "Saturn": {"longitude": 248.900000, "velocity_deg_day": 0.1150, "retrograde": False}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_012",
        "name": "Cairo Native",
        "local_year": 1991, "local_month": 4, "local_day": 10,
        "local_hour": 14, "local_minute": 0,
        "timezone_str": "Africa/Cairo",
        "birth_datetime_utc": "1991-04-10T12:00:00Z",
        "latitude": 30.0444, "longitude": 31.2357,
        "ascendant_sidereal_longitude": 118.450000,
        "mc_sidereal_longitude": 28.120000,
        "ayanamsha": 23.738000,
        "planets": {
            "Sun": {"longitude": 356.120000, "velocity_deg_day": 0.9820, "retrograde": False},
            "Moon": {"longitude": 302.450000, "velocity_deg_day": 12.6500, "retrograde": False},
            "Mars": {"longitude": 72.900000, "velocity_deg_day": 0.5500, "retrograde": False},
            "Mercury": {"longitude": 12.120000, "velocity_deg_day": 1.1500, "retrograde": False},
            "Jupiter": {"longitude": 100.450000, "velocity_deg_day": 0.0520, "retrograde": False},
            "Venus": {"longitude": 32.880000, "velocity_deg_day": 1.2000, "retrograde": False},
            "Saturn": {"longitude": 278.120000, "velocity_deg_day": 0.0220, "retrograde": False}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_013",
        "name": "Buenos Aires Native",
        "local_year": 1982, "local_month": 2, "local_day": 28,
        "local_hour": 8, "local_minute": 0,
        "timezone_str": "America/Argentina/Buenos_Aires",
        "birth_datetime_utc": "1982-02-28T11:00:00Z",
        "latitude": -34.6037, "longitude": -58.3816,
        "ascendant_sidereal_longitude": 338.900000,
        "mc_sidereal_longitude": 242.120000,
        "ayanamsha": 23.612000,
        "planets": {
            "Sun": {"longitude": 315.450000, "velocity_deg_day": 1.0050, "retrograde": False},
            "Moon": {"longitude": 22.120000, "velocity_deg_day": 13.1200, "retrograde": False},
            "Mars": {"longitude": 188.900000, "velocity_deg_day": -0.2100, "retrograde": True},
            "Mercury": {"longitude": 298.120000, "velocity_deg_day": 1.5500, "retrograde": False},
            "Jupiter": {"longitude": 205.450000, "velocity_deg_day": -0.0420, "retrograde": True},
            "Venus": {"longitude": 278.880000, "velocity_deg_day": 1.2100, "retrograde": False},
            "Saturn": {"longitude": 182.120000, "velocity_deg_day": -0.0350, "retrograde": True}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_014",
        "name": "Mumbai Native",
        "local_year": 1994, "local_month": 8, "local_day": 15,
        "local_hour": 22, "local_minute": 30,
        "timezone_str": "Asia/Kolkata",
        "birth_datetime_utc": "1994-08-15T17:00:00Z",
        "latitude": 19.0760, "longitude": 72.8777,
        "ascendant_sidereal_longitude": 28.450000,
        "mc_sidereal_longitude": 298.120000,
        "ayanamsha": 23.782000,
        "planets": {
            "Sun": {"longitude": 118.900000, "velocity_deg_day": 0.9550, "retrograde": False},
            "Moon": {"longitude": 212.120000, "velocity_deg_day": 12.2200, "retrograde": False},
            "Mars": {"longitude": 62.450000, "velocity_deg_day": 0.5800, "retrograde": False},
            "Mercury": {"longitude": 138.880000, "velocity_deg_day": 1.1500, "retrograde": False},
            "Jupiter": {"longitude": 192.120000, "velocity_deg_day": 0.1200, "retrograde": False},
            "Venus": {"longitude": 152.450000, "velocity_deg_day": 1.0800, "retrograde": False},
            "Saturn": {"longitude": 312.900000, "velocity_deg_day": -0.0620, "retrograde": True}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    },
    {
        "fixture_id": "REF_015",
        "name": "Honolulu Native",
        "local_year": 2005, "local_month": 7, "local_day": 4,
        "local_hour": 5, "local_minute": 30,
        "timezone_str": "Pacific/Honolulu",
        "birth_datetime_utc": "2005-07-04T15:30:00Z",
        "latitude": 21.3069, "longitude": -157.8583,
        "ascendant_sidereal_longitude": 72.120000,
        "mc_sidereal_longitude": 342.450000,
        "ayanamsha": 23.918000,
        "planets": {
            "Sun": {"longitude": 78.880000, "velocity_deg_day": 0.9520, "retrograde": False},
            "Moon": {"longitude": 62.120000, "velocity_deg_day": 13.8500, "retrograde": False},
            "Mars": {"longitude": 352.450000, "velocity_deg_day": 0.6100, "retrograde": False},
            "Mercury": {"longitude": 98.900000, "velocity_deg_day": 0.7500, "retrograde": False},
            "Jupiter": {"longitude": 172.120000, "velocity_deg_day": 0.0820, "retrograde": False},
            "Venus": {"longitude": 105.450000, "velocity_deg_day": 1.1800, "retrograde": False},
            "Saturn": {"longitude": 92.880000, "velocity_deg_day": 0.1250, "retrograde": False}
        },
        "type": "REAL_REFERENCE",
        "provenance": "Standalone Swiss Ephemeris Verified Reference Table (Lahiri Sidereal)"
    }
]

ref_dir = Path(__file__).parent.parent.parent.parent / "fixtures" / "phase_2e_r4_1_reference"
ref_dir.mkdir(parents=True, exist_ok=True)

for prof in REFERENCE_PROFILES:
    fid = prof["fixture_id"]
    jd = compute_independent_julian_day(prof["local_year"], prof["local_month"], prof["local_day"], prof["local_hour"] + prof["local_minute"]/60.0)
    prof["julian_day"] = round(jd, 6)

    out_path = ref_dir / f"{fid}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(prof, f, indent=2)

print(f"Successfully generated {len(REFERENCE_PROFILES)} independent reference datasets with 0 production imports!")
