"""
Reference data and authoritative ephemeris benchmark fixtures for Astrovision Phase 1B.
"""

REFERENCE_CASES = [
    {
        "case_id": "SUBRAMANIAN_TS",
        "name": "Subramanian T S",
        "dob": "1986-09-28",
        "time": "16:30",
        "tz": "Asia/Kolkata",
        "place": "Palakkad, Kerala",
        "lat": 10.7867,
        "lon": 76.6548,
        "expected_ascendant_sign": "Aquarius",
        "expected_ascendant_deg": 11.195, # ~11°11'42"
        "expected_mc_sign": "Scorpio",
        "expected_mc_deg": 16.537,     # ~16°32'16"
        "expected_moon_sign": "Cancer",
        "expected_moon_deg": 7.015,     # ~07°00'56"
        "expected_nakshatra": "Pushya",
        "expected_pada": 2
    },
    {
        "case_id": "KOCHI_1990",
        "name": "User A",
        "dob": "1990-01-15",
        "time": "08:30",
        "tz": "Asia/Kolkata",
        "place": "Kochi, India",
        "lat": 9.9312,
        "lon": 76.2673
    },
    {
        "case_id": "LONDON_1985",
        "name": "User B",
        "dob": "1985-07-22",
        "time": "18:45",
        "tz": "Europe/London",
        "place": "London, UK",
        "lat": 51.5074,
        "lon": -0.1278
    },
    {
        "case_id": "GREENWICH_2000",
        "name": "J2000 Epoch",
        "dob": "2000-01-01",
        "time": "12:00",
        "tz": "UTC",
        "place": "Greenwich",
        "lat": 51.4769,
        "lon": 0.0
    }
]
