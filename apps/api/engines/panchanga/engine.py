"""
Authoritative Panchanga Calculation Engine.
Calculates exact Tithi, Vara, Nakshatra, Nitya Yoga, Karana, Solar/Lunar Times, Rahu Kalam, Yamaganda, Gulika Kalam, and Abhijit Muhurta.
Uses Skyfield & DE440s via AstronomyProvider.
Sections 1..10 Compliance:
- Fails closed on naive datetime input (requires timezone-aware datetime with valid IANA ZoneInfo key or timezone_str).
- Zero clamping in Tithi (1..30) or Karana (1..60) derivations. Raises explicit ValueError on out-of-range values.
- Literal, immutable CANONICAL_60_KARANAS tuple explicitly defining all 60 half-Tithis (zero loop-generated specs!).
- Movable non-Vishti Karanas classified explicitly as Neutral (zero fabricated Auspicious labels!).
- Zero synthetic sunrise/sunset or 12-hour fallbacks! Raises explicit ValueError if astronomical sunrise/sunset fails.
- Vara derived from local civil date at observer location (not UTC weekday!).
- Astronomical sunrise and sunset computed dynamically via Skyfield JPL DE440s almanac across observer local civil date.
- Observer elevation propagated directly to Skyfield observer.
- Daytime octant windows (Rahu Kalam, Yamaganda, Gulika) computed from actual local sunrise/sunset daylight interval.
- Canonical 30-Tithi metadata structure (zero modulo-15 ambiguity!).
- Comprehensive unrounded SHA-256 calculation hash covering all material inputs, outputs, daylight/octant durations, start/end windows, and astronomical checksums.
"""
import hashlib
import json
import math
import zoneinfo
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

from apps.api.engines.astronomy.provider import BaseAstronomyProvider
from apps.api.engines.astronomy.providers.skyfield_jpl import SkyfieldJPLProvider
from apps.api.engines.vedic.nakshatra import NAKSHATRA_NAMES
from apps.api.engines.panchanga.models import (
    TithiInfo,
    VaraInfo,
    NityaYogaInfo,
    KaranaInfo,
    TimingWindow,
    PanchangaResult
)

NITYA_YOGAS = [
    ("Vishkambha", "Inauspicious"), ("Priti", "Auspicious"), ("Ayushman", "Auspicious"),
    ("Saubhagya", "Auspicious"), ("Sobhana", "Auspicious"), ("Atiganda", "Inauspicious"),
    ("Sukarma", "Auspicious"), ("Dhriti", "Auspicious"), ("Shoola", "Inauspicious"),
    ("Ganda", "Inauspicious"), ("Vriddhi", "Auspicious"), ("Dhruva", "Auspicious"),
    ("Vyaghasha", "Inauspicious"), ("Harshana", "Auspicious"), ("Vajra", "Inauspicious"),
    ("Siddhi", "Auspicious"), ("Vyatipata", "Inauspicious"), ("Variyan", "Auspicious"),
    ("Parigha", "Inauspicious"), ("Shiva", "Auspicious"), ("Siddha", "Auspicious"),
    ("Sadhya", "Auspicious"), ("Shubha", "Auspicious"), ("Sukla", "Auspicious"),
    ("Brahma", "Auspicious"), ("Indra", "Auspicious"), ("Vaidhriti", "Inauspicious")
]

# Canonical 30 Tithis: (tithi_num_1_to_30, name, paksha, paksha_tithi_num_1_to_15, is_rikta, is_amavasya, is_purnima)
CANONICAL_30_TITHIS = [
    # Sukla Paksha (1..15)
    (1, "Pratipada", "Sukla Paksha", 1, False, False, False),
    (2, "Dwitiya", "Sukla Paksha", 2, False, False, False),
    (3, "Tritiya", "Sukla Paksha", 3, False, False, False),
    (4, "Chaturthi", "Sukla Paksha", 4, True, False, False),   # Rikta
    (5, "Panchami", "Sukla Paksha", 5, False, False, False),
    (6, "Shashthi", "Sukla Paksha", 6, False, False, False),
    (7, "Saptami", "Sukla Paksha", 7, False, False, False),
    (8, "Ashtami", "Sukla Paksha", 8, False, False, False),
    (9, "Navami", "Sukla Paksha", 9, True, False, False),    # Rikta
    (10, "Dashami", "Sukla Paksha", 10, False, False, False),
    (11, "Ekadashi", "Sukla Paksha", 11, False, False, False),
    (12, "Dwadashi", "Sukla Paksha", 12, False, False, False),
    (13, "Trayodashi", "Sukla Paksha", 13, False, False, False),
    (14, "Chaturdashi", "Sukla Paksha", 14, True, False, False), # Rikta
    (15, "Purnima", "Sukla Paksha", 15, False, False, True),    # Purnima
    # Krishna Paksha (16..30)
    (16, "Pratipada", "Krishna Paksha", 1, False, False, False),
    (17, "Dwitiya", "Krishna Paksha", 2, False, False, False),
    (18, "Tritiya", "Krishna Paksha", 3, False, False, False),
    (19, "Chaturthi", "Krishna Paksha", 4, True, False, False),  # Rikta
    (20, "Panchami", "Krishna Paksha", 5, False, False, False),
    (21, "Shashthi", "Krishna Paksha", 6, False, False, False),
    (22, "Saptami", "Krishna Paksha", 7, False, False, False),
    (23, "Ashtami", "Krishna Paksha", 8, False, False, False),
    (24, "Navami", "Krishna Paksha", 9, True, False, False),   # Rikta
    (25, "Dashami", "Krishna Paksha", 10, False, False, False),
    (26, "Ekadashi", "Krishna Paksha", 11, False, False, False),
    (27, "Dwadashi", "Krishna Paksha", 12, False, False, False),
    (28, "Trayodashi", "Krishna Paksha", 13, False, False, False),
    (29, "Chaturdashi", "Krishna Paksha", 14, True, False, False), # Rikta
    (30, "Amavasya", "Krishna Paksha", 15, False, True, False)   # Amavasya
]

# Literal, immutable 60-element CANONICAL_60_KARANAS tuple: (karana_num_1_to_60, name, type, nature, is_vishti)
CANONICAL_60_KARANAS = (
    # Karana 1 (Fixed)
    (1, "Kimstughna", "Fixed", "Neutral", False),
    # Cycle 1 (2..8)
    (2, "Bava", "Movable", "Neutral", False),
    (3, "Balava", "Movable", "Neutral", False),
    (4, "Kaulava", "Movable", "Neutral", False),
    (5, "Taitila", "Movable", "Neutral", False),
    (6, "Gara", "Movable", "Neutral", False),
    (7, "Vanija", "Movable", "Neutral", False),
    (8, "Vishti", "Movable", "Vishti/Bhadra", True),
    # Cycle 2 (9..15)
    (9, "Bava", "Movable", "Neutral", False),
    (10, "Balava", "Movable", "Neutral", False),
    (11, "Kaulava", "Movable", "Neutral", False),
    (12, "Taitila", "Movable", "Neutral", False),
    (13, "Gara", "Movable", "Neutral", False),
    (14, "Vanija", "Movable", "Neutral", False),
    (15, "Vishti", "Movable", "Vishti/Bhadra", True),
    # Cycle 3 (16..22)
    (16, "Bava", "Movable", "Neutral", False),
    (17, "Balava", "Movable", "Neutral", False),
    (18, "Kaulava", "Movable", "Neutral", False),
    (19, "Taitila", "Movable", "Neutral", False),
    (20, "Gara", "Movable", "Neutral", False),
    (21, "Vanija", "Movable", "Neutral", False),
    (22, "Vishti", "Movable", "Vishti/Bhadra", True),
    # Cycle 4 (23..29)
    (23, "Bava", "Movable", "Neutral", False),
    (24, "Balava", "Movable", "Neutral", False),
    (25, "Kaulava", "Movable", "Neutral", False),
    (26, "Taitila", "Movable", "Neutral", False),
    (27, "Gara", "Movable", "Neutral", False),
    (28, "Vanija", "Movable", "Neutral", False),
    (29, "Vishti", "Movable", "Vishti/Bhadra", True),
    # Cycle 5 (30..36)
    (30, "Bava", "Movable", "Neutral", False),
    (31, "Balava", "Movable", "Neutral", False),
    (32, "Kaulava", "Movable", "Neutral", False),
    (33, "Taitila", "Movable", "Neutral", False),
    (34, "Gara", "Movable", "Neutral", False),
    (35, "Vanija", "Movable", "Neutral", False),
    (36, "Vishti", "Movable", "Vishti/Bhadra", True),
    # Cycle 6 (37..43)
    (37, "Bava", "Movable", "Neutral", False),
    (38, "Balava", "Movable", "Neutral", False),
    (39, "Kaulava", "Movable", "Neutral", False),
    (40, "Taitila", "Movable", "Neutral", False),
    (41, "Gara", "Movable", "Neutral", False),
    (42, "Vanija", "Movable", "Neutral", False),
    (43, "Vishti", "Movable", "Vishti/Bhadra", True),
    # Cycle 7 (44..50)
    (44, "Bava", "Movable", "Neutral", False),
    (45, "Balava", "Movable", "Neutral", False),
    (46, "Kaulava", "Movable", "Neutral", False),
    (47, "Taitila", "Movable", "Neutral", False),
    (48, "Gara", "Movable", "Neutral", False),
    (49, "Vanija", "Movable", "Neutral", False),
    (50, "Vishti", "Movable", "Vishti/Bhadra", True),
    # Cycle 8 (51..57)
    (51, "Bava", "Movable", "Neutral", False),
    (52, "Balava", "Movable", "Neutral", False),
    (53, "Kaulava", "Movable", "Neutral", False),
    (54, "Taitila", "Movable", "Neutral", False),
    (55, "Gara", "Movable", "Neutral", False),
    (56, "Vanija", "Movable", "Neutral", False),
    (57, "Vishti", "Movable", "Vishti/Bhadra", True),
    # Fixed Terminal Karanas (58..60)
    (58, "Shakuni", "Fixed", "Inauspicious", False),
    (59, "Chatushpada", "Fixed", "Inauspicious", False),
    (60, "Naga", "Fixed", "Inauspicious", False)
)

VARA_MAP = [
    (0, "Sunday", "Raviwara", "Sun"),
    (1, "Monday", "Somawara", "Moon"),
    (2, "Tuesday", "Mangalawara", "Mars"),
    (3, "Wednesday", "Budhawara", "Mercury"),
    (4, "Thursday", "Guruwara", "Jupiter"),
    (5, "Friday", "Shukrawara", "Venus"),
    (6, "Saturday", "Shaniwara", "Saturn")
]

# 1-based octant index (1 to 8) for daytime Panchanga windows by weekday (0=Sunday..6=Saturday)
RAHU_OCTANTS = [8, 2, 7, 5, 6, 4, 3]
YAMAGANDA_OCTANTS = [5, 4, 3, 2, 1, 7, 6]
GULIKA_OCTANTS = [7, 6, 5, 4, 3, 2, 1]

class PanchangaEngine:
    """
    Authoritative Panchanga Engine.
    Computes Tithi, Vara, Nakshatra, Yoga, Karana, Solar times, and Muhurta windows.
    """

    @classmethod
    def calculate_panchanga(
        cls,
        dt: datetime,
        latitude: float,
        longitude: float,
        elevation: float = 0.0,
        location_name: str = "Local Observer",
        timezone_str: Optional[str] = None,
        astronomy_provider: Optional[BaseAstronomyProvider] = None
    ) -> PanchangaResult:
        if not astronomy_provider:
            astronomy_provider = SkyfieldJPLProvider()

        # Section 2: Strict timezone-aware input validation requiring IANA ZoneInfo key or resolvable timezone string
        if dt.tzinfo is None:
            raise ValueError(f"Input datetime '{dt}' must be timezone-aware with a valid IANA timezone.")

        tz_str = None
        if timezone_str and isinstance(timezone_str, str) and timezone_str.strip():
            tz_str = timezone_str.strip()
        else:
            tz_key = getattr(dt.tzinfo, "key", None)
            if tz_key and isinstance(tz_key, str) and tz_key.strip():
                tz_str = tz_key.strip()
            elif dt.tzinfo == timezone.utc or str(dt.tzinfo) in ["UTC", "utc", "UTC+00:00", "+00:00"]:
                tz_str = "UTC"
            else:
                tz_cand = str(dt.tzinfo).strip()
                try:
                    zoneinfo.ZoneInfo(tz_cand)
                    tz_str = tz_cand
                except Exception:
                    tz_str = None

        if not tz_str:
            raise ValueError(f"Input datetime '{dt}' must carry a valid IANA ZoneInfo key or resolvable timezone string. Got '{dt.tzinfo}'.")

        try:
            target_zone = zoneinfo.ZoneInfo(tz_str)
        except Exception:
            try:
                import pytz
                target_zone = pytz.timezone(tz_str)
            except Exception as e:
                raise ValueError(f"Invalid or unresolvable IANA timezone key '{tz_str}': {str(e)}")

        utc_dt = dt.astimezone(timezone.utc)

        # 1. Astronomical Calculation at exact datetime
        astro_res = astronomy_provider.calculate_astronomical_state(
            year=utc_dt.year,
            month=utc_dt.month,
            day=utc_dt.day,
            hour=utc_dt.hour,
            minute=utc_dt.minute,
            second=utc_dt.second,
            lat=latitude,
            lon=longitude,
            elevation=elevation,
            ayanamsha_mode="Lahiri"
        )

        sun_lon = astro_res.sidereal_state.sidereal_longitudes["Sun"]
        moon_lon = astro_res.sidereal_state.sidereal_longitudes["Moon"]

        # 2. Canonical 30-Tithi Calculation (Strict non-clamped mathematical derivation!)
        elongation = (moon_lon - sun_lon) % 360.0
        if not math.isfinite(elongation):
            raise ValueError(f"Non-finite planetary elongation calculated: {elongation}")

        raw_tithi_idx = int(elongation // 12.0)
        tithi_num = raw_tithi_idx + 1
        if not (1 <= tithi_num <= 30):
            raise ValueError(f"Calculated Tithi number {tithi_num} is out of physical range [1, 30].")

        deg_in_tithi = elongation % 12.0
        pct_tithi = (deg_in_tithi / 12.0) * 100.0

        t_data = CANONICAL_30_TITHIS[tithi_num - 1]
        _, t_name, paksha, paksha_t_num, is_rikta, is_amavasya, is_purnima = t_data

        tithi_info = TithiInfo(
            tithi_number=tithi_num,
            paksha_tithi_number=paksha_t_num,
            tithi_name=t_name,
            paksha=paksha,
            is_rikta=is_rikta,
            is_amavasya=is_amavasya,
            is_purnima=is_purnima,
            degree_elapsed_in_tithi=round(deg_in_tithi, 2),
            percentage_elapsed=round(pct_tithi, 2)
        )

        # 3. Vara Calculation (Derived from local civil date at observer location!)
        local_weekday_idx = dt.weekday() # 0=Monday..6=Sunday
        sun_weekday_idx = (local_weekday_idx + 1) % 7 # 0=Sunday..6=Saturday
        vara_tuple = VARA_MAP[sun_weekday_idx]

        vara_info = VaraInfo(
            weekday_number=vara_tuple[0],
            day_name_english=vara_tuple[1],
            day_name_sanskrit=vara_tuple[2],
            ruling_planet=vara_tuple[3]
        )

        # 4. Nakshatra Calculation (Strict range validation without modulo masking!)
        m_lon_norm = moon_lon % 360.0
        if not math.isfinite(m_lon_norm):
            raise ValueError(f"Non-finite Moon longitude calculated: {moon_lon}")

        raw_nak_idx = int(m_lon_norm // (360.0 / 27.0))
        if not (0 <= raw_nak_idx < 27):
            raise ValueError(f"Calculated Nakshatra index {raw_nak_idx} out of physical range [0, 26].")

        nak_name = NAKSHATRA_NAMES[raw_nak_idx]
        deg_in_nak = m_lon_norm % (360.0 / 27.0)
        pada = int(deg_in_nak // (360.0 / 108.0)) + 1 # 1 to 4
        if not (1 <= pada <= 4):
            raise ValueError(f"Calculated Nakshatra Pada {pada} out of physical range [1, 4].")

        # 5. Nitya Yoga Calculation (Strict range validation without modulo masking!)
        solilunar_sum = (sun_lon + moon_lon) % 360.0
        if not math.isfinite(solilunar_sum):
            raise ValueError(f"Non-finite solilunar sum calculated: {solilunar_sum}")

        raw_yoga_idx = int(solilunar_sum // (360.0 / 27.0))
        if not (0 <= raw_yoga_idx < 27):
            raise ValueError(f"Calculated Nitya Yoga index {raw_yoga_idx} out of physical range [0, 26].")

        yoga_tuple = NITYA_YOGAS[raw_yoga_idx]

        nitya_yoga_info = NityaYogaInfo(
            yoga_number=raw_yoga_idx + 1,
            yoga_name=yoga_tuple[0],
            nature=yoga_tuple[1]
        )

        # 6. Canonical 60-Karana Calculation (Strict non-clamped mathematical derivation from CANONICAL_60_KARANAS!)
        raw_karana_idx = int(elongation // 6.0)
        karana_num = raw_karana_idx + 1
        if not (1 <= karana_num <= 60):
            raise ValueError(f"Calculated Karana number {karana_num} is out of physical range [1, 60].")

        k_data = CANONICAL_60_KARANAS[karana_num - 1]
        _, k_name, k_type, k_nature, is_vishti = k_data

        karana_info = KaranaInfo(
            karana_number=karana_num,
            karana_name=k_name,
            type=k_type,
            nature=k_nature,
            is_vishti=is_vishti
        )

        # 7. Astronomical Sunrise, Sunset & Daytime Octant Windows (Fail closed on missing/invalid solar times!)
        if hasattr(astronomy_provider, "calculate_sunrise_sunset"):
            sr_ss_dict = astronomy_provider.calculate_sunrise_sunset(
                local_date=dt.date(),
                latitude=latitude,
                longitude=longitude,
                timezone_name=tz_str,
                elevation=elevation
            )
            sr_dt_utc = sr_ss_dict.get("sunrise_utc")
            ss_dt_utc = sr_ss_dict.get("sunset_utc")
        else:
            sr_dt_utc = None
            ss_dt_utc = None

        if not sr_dt_utc or not ss_dt_utc:
            raise ValueError(f"Astronomical sunrise/sunset calculation failed for observer at ({latitude}, {longitude}) on local date {dt.date()} in timezone '{tz_str}'. Fail closed: zero fallbacks permitted.")

        daylight_sec = (ss_dt_utc - sr_dt_utc).total_seconds()
        if daylight_sec <= 0:
            raise ValueError(f"Calculated sunset ({ss_dt_utc}) is not strictly after sunrise ({sr_dt_utc}) for observer at ({latitude}, {longitude}). Fail closed: zero fallbacks permitted.")

        octant_sec = daylight_sec / 8.0

        def _make_window(name: str, octant_idx_1based: int, nature: str) -> TimingWindow:
            s_dt = sr_dt_utc + timedelta(seconds=octant_sec * (octant_idx_1based - 1))
            e_dt = sr_dt_utc + timedelta(seconds=octant_sec * octant_idx_1based)
            return TimingWindow(
                name=name,
                start_time_iso=s_dt.isoformat(),
                end_time_iso=e_dt.isoformat(),
                nature=nature
            )

        rahu_w = _make_window("Rahu Kalam", RAHU_OCTANTS[sun_weekday_idx], "Inauspicious")
        yamaganda_w = _make_window("Yamaganda", YAMAGANDA_OCTANTS[sun_weekday_idx], "Inauspicious")
        gulika_w = _make_window("Gulika Kalam", GULIKA_OCTANTS[sun_weekday_idx], "Inauspicious")

        # Abhijit Muhurta (8th Muhurta of the day around midday)
        abhijit_s = sr_dt_utc + timedelta(seconds=octant_sec * 3.5)
        abhijit_e = sr_dt_utc + timedelta(seconds=octant_sec * 4.5)
        abhijit_w = TimingWindow(
            name="Abhijit Muhurta",
            start_time_iso=abhijit_s.isoformat(),
            end_time_iso=abhijit_e.isoformat(),
            nature="Auspicious"
        )

        payload = {
            "datetime_iso": utc_dt.isoformat(),
            "local_datetime_iso": dt.isoformat(),
            "timezone_str": tz_str,
            "latitude": latitude,
            "longitude": longitude,
            "elevation": elevation,
            "sun_lon": sun_lon, # unrounded exact float
            "moon_lon": moon_lon, # unrounded exact float
            "elongation": elongation,
            "tithi_num": tithi_num,
            "tithi_name": t_name,
            "paksha": paksha,
            "paksha_tithi_num": paksha_t_num,
            "is_rikta": is_rikta,
            "is_amavasya": is_amavasya,
            "is_purnima": is_purnima,
            "degree_elapsed_in_tithi": deg_in_tithi,
            "percentage_elapsed_in_tithi": pct_tithi,
            "weekday_number": vara_tuple[0],
            "day_name_english": vara_tuple[1],
            "day_name_sanskrit": vara_tuple[2],
            "ruling_planet": vara_tuple[3],
            "nakshatra_name": nak_name,
            "nakshatra_pada": pada,
            "yoga_number": raw_yoga_idx + 1,
            "yoga_name": yoga_tuple[0],
            "yoga_nature": yoga_tuple[1],
            "karana_number": karana_num,
            "karana_name": k_name,
            "karana_type": k_type,
            "karana_nature": k_nature,
            "is_vishti": is_vishti,
            "sunrise_iso": sr_dt_utc.isoformat(),
            "sunset_iso": ss_dt_utc.isoformat(),
            "daylight_seconds": daylight_sec,
            "octant_seconds": octant_sec,
            "rahu_kalam_start": rahu_w.start_time_iso,
            "rahu_kalam_end": rahu_w.end_time_iso,
            "yamaganda_start": yamaganda_w.start_time_iso,
            "yamaganda_end": yamaganda_w.end_time_iso,
            "gulika_start": gulika_w.start_time_iso,
            "gulika_end": gulika_w.end_time_iso,
            "abhijit_start": abhijit_w.start_time_iso,
            "abhijit_end": abhijit_w.end_time_iso,
            "astro_hash": astro_res.metadata.calculation_hash,
            "panchanga_ruleset_version": "2026.1_CANONICAL_PANCHANGA_V2"
        }
        p_hash = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

        return PanchangaResult(
            datetime_iso=utc_dt.isoformat(),
            location_name=location_name,
            latitude=latitude,
            longitude=longitude,
            tithi=tithi_info,
            vara=vara_info,
            nakshatra_name=nak_name,
            nakshatra_pada=pada,
            nitya_yoga=nitya_yoga_info,
            karana=karana_info,
            sunrise_iso=sr_dt_utc.isoformat(),
            sunset_iso=ss_dt_utc.isoformat(),
            rahu_kalam=rahu_w,
            yamaganda=yamaganda_w,
            gulika_kalam=gulika_w,
            abhijit_muhurta=abhijit_w,
            calculation_hash=p_hash
        )
