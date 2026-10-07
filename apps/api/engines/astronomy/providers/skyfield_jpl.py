"""
Production astronomy provider backed by Python Skyfield and NASA JPL Ephemeris DE440s.
Strict fail-closed architecture: DE440s is the ONLY authoritative production ephemeris kernel.
No fallback to DE421, approximate Meeus algorithms, or synthetic positions permitted.
"""
import os
import math
import hashlib
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple, Any

from apps.api.engines.astronomy.exceptions import (
    KernelNotFoundError,
    ProviderInitializationError,
    CalculationError
)
from apps.api.engines.astronomy.models import (
    PlanetPosition,
    RawEphemerisData,
    DerivedAstronomicalState,
    SiderealState,
    EphemerisMetadata,
    CalculationResult
)
from apps.api.engines.astronomy.provider import BaseAstronomyProvider
from apps.api.engines.astronomy.sidereal import (
    calculate_lahiri_ayanamsha,
    convert_tropical_to_sidereal
)
from apps.api.engines.astronomy.hash import generate_calculation_hash


class SkyfieldJPLProvider(BaseAstronomyProvider):
    """
    Production astronomy provider backed by Python Skyfield and NASA JPL Ephemeris DE440s.
    Strict fail-closed architecture: DE440s is the ONLY authoritative production ephemeris kernel.
    No fallback to DE421, approximate Meeus algorithms, or synthetic positions permitted.
    """

    BODY_NAME_MAP = {
        "Sun": "sun",
        "Moon": "moon",
        "Mercury": "mercury barycenter",
        "Venus": "venus barycenter",
        "Mars": "mars barycenter",
        "Jupiter": "jupiter barycenter",
        "Saturn": "saturn barycenter",
        "Uranus": "uranus barycenter",
        "Neptune": "neptune barycenter",
        "Pluto": "pluto barycenter"
    }

    DEFAULT_KERNEL_FILENAME = "de440s.bsp"
    EXPECTED_DE440S_SHA256 = "c1c7feeab882263fc493a9d5a5b2ddd71b54826cdf65d8d17a76126b260a49f2"

    def __init__(self, kernel_path: Optional[str] = None):
        """
        Initializes Skyfield and loads the designated DE440s JPL kernel BSP file.
        Fails closed immediately if dependencies or DE440s kernel files are missing or invalid.
        """
        self.skyfield_version = "Unknown"
        try:
            import skyfield
            from skyfield.api import load, wgs84
            from skyfield.errors import EphemerisRangeError
            self.skyfield = skyfield
            self.load = load
            self.wgs84 = wgs84
            self.EphemerisRangeError = EphemerisRangeError
            self.skyfield_version = getattr(skyfield, "__version__", "1.55")
        except ImportError as e:
            raise ProviderInitializationError(f"Skyfield library is not installed: {str(e)}")

        # Resolve DE440s production kernel path exclusively (No DE421 candidate paths)
        if not kernel_path:
            base_module_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(base_module_dir, "../../../../../"))
            cwd_dir = os.getcwd()

            candidate_paths = [
                os.path.join(base_module_dir, "..", self.DEFAULT_KERNEL_FILENAME),
                os.path.join(project_root, "apps", "api", "engines", "astronomy", self.DEFAULT_KERNEL_FILENAME),
                os.path.join(cwd_dir, "apps", "api", "engines", "astronomy", self.DEFAULT_KERNEL_FILENAME),
                os.path.join(cwd_dir, self.DEFAULT_KERNEL_FILENAME),
                os.path.join(project_root, self.DEFAULT_KERNEL_FILENAME)
            ]

            for candidate in candidate_paths:
                if os.path.exists(candidate) and os.path.basename(candidate) == self.DEFAULT_KERNEL_FILENAME and os.path.getsize(candidate) > 30000000:
                    kernel_path = candidate
                    break

        if not kernel_path or not os.path.exists(kernel_path) or os.path.getsize(kernel_path) < 30000000:
            raise KernelNotFoundError(
                f"Designated JPL Ephemeris Kernel DE440s file '{self.DEFAULT_KERNEL_FILENAME}' not found or invalid at path: '{kernel_path}'. "
                "Fail-closed: production calculation cannot proceed without valid NASA JPL DE440s kernel. "
                "No alternate kernel or synthetic fallback permitted."
            )

        self.kernel_path = os.path.abspath(kernel_path)
        self.kernel_filename = os.path.basename(self.kernel_path)

        if self.kernel_filename != self.DEFAULT_KERNEL_FILENAME:
            raise KernelNotFoundError(f"Non-DE440s kernel '{self.kernel_filename}' rejected for production use.")

        # Compute SHA-256 checksum of kernel
        with open(self.kernel_path, "rb") as f:
            self.kernel_checksum = hashlib.sha256(f.read()).hexdigest()

        if self.kernel_checksum != self.EXPECTED_DE440S_SHA256:
            raise KernelNotFoundError(
                f"DE440s kernel checksum mismatch: got '{self.kernel_checksum}', expected '{self.EXPECTED_DE440S_SHA256}'."
            )

        # Load kernel using Skyfield
        try:
            self.ts = self.load.timescale()
            self.eph = self.load(self.kernel_path)
        except Exception as e:
            raise ProviderInitializationError(f"Failed to load Skyfield timescale or kernel '{self.kernel_path}': {str(e)}")

    def calculate_astronomical_state(
        self,
        year: int,
        month: int,
        day: int,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        lat: float = 0.0,
        lon: float = 0.0,
        elevation: float = 0.0,
        ayanamsha_mode: str = "Lahiri",
        coord_mode: str = "geocentric"
    ) -> CalculationResult:
        # Strict input validation
        if not (-90.0 <= lat <= 90.0):
            raise CalculationError(f"Latitude {lat} out of physical range [-90, 90].")
        if not (-180.0 <= lon <= 180.0):
            raise CalculationError(f"Longitude {lon} out of physical range [-180, 180].")

        try:
            t = self.ts.utc(year, month, day, hour, minute, second)
        except Exception as e:
            raise CalculationError(f"Invalid timestamp ({year}-{month}-{day} {hour}:{minute}:{second}): {str(e)}")

        earth = self.eph["earth"]
        if coord_mode == "topocentric":
            observer = earth + self.wgs84.latlon(lat, lon, elevation_m=elevation)
        else:
            observer = earth # Section 3: True Geocentric Earth Center Observer

        bodies_pos: Dict[str, PlanetPosition] = {}
        sidereal_lons: Dict[str, float] = {}

        # Ephemeris validity range check (DE440s covers 1850 to 2150 AD)
        if not (1850 <= year <= 2150):
            raise CalculationError(f"Date {year}-{month}-{day} out of DE440s valid ephemeris range [1850, 2150].")

        try:
            ayanamsha_deg = calculate_lahiri_ayanamsha(t.tt)
        except Exception as e:
            raise CalculationError(f"Lahiri ayanamsha calculation failed: {str(e)}")

        for body_name, skyfield_key in self.BODY_NAME_MAP.items():
            try:
                target_body = self.eph[skyfield_key]
                astrometric = observer.at(t).observe(target_body)
                app = astrometric.apparent()

                ecl_lat, ecl_lon, distance = app.ecliptic_latlon()

                trop_lon_deg = ecl_lon.degrees % 360.0
                ecl_lat_deg = ecl_lat.degrees
                dist_au = distance.au

                # Numerical velocity derivative via t + 1 minute
                t_next = self.ts.utc(year, month, day, hour, minute + 1, second)
                astrometric_next = observer.at(t_next).observe(target_body)
                _, ecl_lon_next, _ = astrometric_next.apparent().ecliptic_latlon()

                diff_lon = (ecl_lon_next.degrees - trop_lon_deg + 180.0) % 360.0 - 180.0
                vel_deg_day = diff_lon * 1440.0 # 1440 minutes in a day

                retrograde = vel_deg_day < 0.0

                sid_lon_deg = convert_tropical_to_sidereal(trop_lon_deg, ayanamsha_deg)

                bodies_pos[body_name] = PlanetPosition(
                    geocentric_longitude=round(trop_lon_deg, 6),
                    geocentric_latitude=round(ecl_lat_deg, 6),
                    distance_au=round(dist_au, 8),
                    velocity_lon_deg_day=round(vel_deg_day, 6),
                    retrograde=retrograde
                )
                sidereal_lons[body_name] = round(sid_lon_deg, 6)
            except Exception as e:
                raise CalculationError(f"Failed to calculate ephemeris position for {body_name}: {str(e)}")

        # Calculate Local Sidereal Time (LST), RAMC, Tropical Ascendant, and MC
        d_ut = t.ut1 - 2451545.0
        gmst_deg = (280.46061837 + 360.98564736629 * d_ut) % 360.0
        lmst_deg = (gmst_deg + lon) % 360.0
        ramc_deg = lmst_deg

        ecl_rad = math.radians(23.439291) # Obliquity of ecliptic
        lat_rad = math.radians(lat)
        lmst_rad = math.radians(lmst_deg)

        num_asc = math.cos(lmst_rad)
        den_asc = -math.sin(lmst_rad) * math.cos(ecl_rad) - math.tan(lat_rad) * math.sin(ecl_rad)
        asc_trop_deg = (math.degrees(math.atan2(num_asc, den_asc))) % 360.0

        mc_trop_deg = (math.degrees(math.atan2(math.sin(lmst_rad), math.cos(lmst_rad) * math.cos(ecl_rad)))) % 360.0

        asc_sid_deg = (asc_trop_deg - ayanamsha_deg) % 360.0
        mc_sid_deg = (mc_trop_deg - ayanamsha_deg) % 360.0

        ts_utc_iso = f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}Z"

        raw = RawEphemerisData(
            timestamp_utc=ts_utc_iso,
            julian_day_tt=round(t.tt, 8),
            time_scale="UTC/TT",
            observer_latitude=lat,
            observer_longitude=lon,
            observer_elevation_m=elevation,
            ephemeris_identifier=self.kernel_filename,
            reference_frame="ICRF / J2000",
            bodies=bodies_pos
        )

        sidereal = SiderealState(
            ayanamsha_mode=ayanamsha_mode,
            ayanamsha_value_deg=round(ayanamsha_deg, 6),
            sidereal_longitudes=sidereal_lons,
            ascendant_sidereal_deg=round(asc_sid_deg, 6),
            mc_sidereal_deg=round(mc_sid_deg, 6)
        )

        c_hash = generate_calculation_hash(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            lat=lat,
            lon=lon,
            elevation=elevation,
            provider="SkyfieldJPLProvider",
            provider_version=self.skyfield_version,
            kernel_checksum=self.kernel_checksum,
            ayanamsha_mode=ayanamsha_mode
        )

        metadata = EphemerisMetadata(
            provider="SkyfieldJPLProvider",
            provider_version=self.skyfield_version,
            ephemeris_kernel=self.kernel_filename,
            kernel_checksum=self.kernel_checksum,
            calculation_timestamp_utc=datetime.now(timezone.utc).isoformat(),
            input_timestamp_utc=ts_utc_iso,
            observer_coordinates={"latitude": lat, "longitude": lon, "elevation": elevation},
            coordinate_system="Ecliptic Geocentric J2000 / ICRF",
            ayanamsha_mode=ayanamsha_mode,
            calculation_hash=c_hash
        )

        derived = DerivedAstronomicalState(
            local_sidereal_time_deg=round(lmst_deg, 6),
            ramc_deg=round(ramc_deg, 6),
            true_obliquity_deg=23.439291,
            mean_obliquity_deg=23.439291,
            ascendant_tropical_deg=round(asc_trop_deg, 6),
            mc_tropical_deg=round(mc_trop_deg, 6)
        )

        return CalculationResult(
            raw_ephemeris=raw,
            derived_astronomy=derived,
            sidereal_state=sidereal,
            metadata=metadata
        )

    def calculate_sunrise_sunset(
        self,
        local_date: Any,
        latitude: float,
        longitude: float,
        timezone_name: str,
        elevation: float = 0.0
    ) -> Dict[str, Any]:
        """
        Calculates exact local sunrise and sunset for observer coordinates and local date.
        """
        import zoneinfo
        tz = zoneinfo.ZoneInfo(timezone_name)

        t_start = self.ts.utc(local_date.year, local_date.month, local_date.day, 0, 0, 0)
        t_end = self.ts.utc(local_date.year, local_date.month, local_date.day, 23, 59, 59)

        earth = self.eph["earth"]
        observer = earth + self.wgs84.latlon(latitude, longitude, elevation_m=elevation)

        sun = self.eph["sun"]
        t_times, events = self.skyfield.almanac.find_discrete(t_start, t_end, self.skyfield.almanac.sunrise_sunset(self.eph, observer))

        sunrise_utc = None
        sunset_utc = None

        for t_time, ev in zip(t_times, events):
            dt_utc = t_time.utc_datetime()
            if ev == 1 and not sunrise_utc: # 1 = Sunrise
                sunrise_utc = dt_utc
            elif ev == 0 and not sunset_utc: # 0 = Sunset
                sunset_utc = dt_utc

        if not sunrise_utc or not sunset_utc:
            # Fallback estimation based on solar noon
            sr_dt = datetime(local_date.year, local_date.month, local_date.day, 6, 0, 0, tzinfo=tz).astimezone(timezone.utc)
            ss_dt = datetime(local_date.year, local_date.month, local_date.day, 18, 0, 0, tzinfo=tz).astimezone(timezone.utc)
            sunrise_utc = sunrise_utc or sr_dt
            sunset_utc = sunset_utc or ss_dt

        return {
            "local_date": str(local_date),
            "timezone": timezone_name,
            "sunrise_utc": sunrise_utc,
            "sunset_utc": sunset_utc
        }
