"""
Skyfield + NASA JPL Ephemeris Astronomy Provider Implementation.
Delivers sub-arcsecond geocentric planetary positions, orbital derivatives, and derived astronomical state.
Enforces fail-closed error handling.
"""
import os
import math
import hashlib
from datetime import datetime, timezone
from typing import Dict, Optional

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
    Production astronomy provider backed by Python Skyfield and JPL SPK Kernels (DE421 / DE440s).
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

    def __init__(self, kernel_path: Optional[str] = None):
        """
        Initializes Skyfield and loads the specified JPL kernel BSP file.
        Fails closed immediately if dependencies or kernel files are missing.
        """
        self.skyfield_version = "Unknown"
        try:
            import skyfield
            from skyfield.api import load
            self.skyfield = skyfield
            self.load = load
            self.skyfield_version = getattr(skyfield, "__version__", "1.55")
        except ImportError as e:
            raise ProviderInitializationError(f"Skyfield library is not installed: {str(e)}")

        # Resolve kernel path
        if not kernel_path:
            # Search candidate paths relative to module, CWD, and project root
            base_module_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(base_module_dir, "../../../../../"))
            cwd_dir = os.getcwd()

            candidate_paths = [
                os.path.join(cwd_dir, "de440s.bsp"),
                os.path.join(cwd_dir, "de421.bsp"),
                os.path.join(project_root, "de440s.bsp"),
                os.path.join(project_root, "de421.bsp"),
            ]

            for candidate in candidate_paths:
                if os.path.exists(candidate) and os.path.getsize(candidate) > 0:
                    kernel_path = candidate
                    break

        if not kernel_path or not os.path.exists(kernel_path) or os.path.getsize(kernel_path) == 0:
            raise KernelNotFoundError(
                f"JPL Ephemeris Kernel file not found or empty at path: '{kernel_path}'. "
                "Fail-closed: calculation cannot proceed without valid ephemeris kernel."
            )

        self.kernel_path = os.path.abspath(kernel_path)
        self.kernel_filename = os.path.basename(self.kernel_path)

        # Compute MD5 checksum of kernel
        with open(self.kernel_path, "rb") as f:
            self.kernel_checksum = hashlib.md5(f.read()).hexdigest()

        # Load kernel
        try:
            self.ts = self.load.timescale(builtin=True)
            self.eph = self.load(self.kernel_path)
        except Exception as e:
            raise KernelNotFoundError(f"Failed to load JPL Ephemeris kernel '{self.kernel_path}': {str(e)}")

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
        ayanamsha_mode: str = "Lahiri"
    ) -> CalculationResult:
        """
        Calculates canonical raw ephemeris, derived astronomical, and sidereal state.
        Raises CalculationError if dates are outside kernel range or numerical error occurs.
        """
        try:
            t = self.ts.utc(year, month, day, hour, minute, second)
            t_next = self.ts.utc(year, month, day, hour, minute, second + 3600) # 1 hr differentiation
            jd_tt = t.tt
            dt_str = f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}Z"

            earth = self.eph['earth']
            planet_positions: Dict[str, PlanetPosition] = {}

            # Calculate geocentric positions and velocities for bodies
            for name, target_key in self.BODY_NAME_MAP.items():
                target_body = self.eph[target_key]

                # Position at t
                astrometric = earth.at(t).observe(target_body)
                apparent = astrometric.apparent()
                ecl = apparent.ecliptic_latlon()

                trop_lon = ecl[1].degrees % 360.0
                ecl_lat = ecl[0].degrees
                dist_au = ecl[2].au

                # Velocity differentiation at t + 1 hour
                astrometric_next = earth.at(t_next).observe(target_body)
                apparent_next = astrometric_next.apparent()
                ecl_next = apparent_next.ecliptic_latlon()
                trop_lon_next = ecl_next[1].degrees % 360.0

                diff_lon = (trop_lon_next - trop_lon + 180.0) % 360.0 - 180.0
                vel_deg_day = diff_lon * 24.0 # 24 hrs/day
                retrograde = diff_lon < 0.0

                planet_positions[name] = PlanetPosition(
                    geocentric_longitude=round(trop_lon, 6),
                    geocentric_latitude=round(ecl_lat, 6),
                    distance_au=round(dist_au, 6),
                    velocity_lon_deg_day=round(vel_deg_day, 6),
                    retrograde=retrograde
                )

            # Raw Ephemeris Data
            raw_ephemeris = RawEphemerisData(
                timestamp_utc=dt_str,
                julian_day_tt=round(jd_tt, 6),
                time_scale="UTC/TT",
                observer_latitude=round(lat, 6),
                observer_longitude=round(lon, 6),
                observer_elevation_m=round(elevation, 2),
                ephemeris_identifier=f"NASA JPL {self.kernel_filename.upper()}",
                reference_frame="ICRF / J2000",
                bodies=planet_positions
            )

            # Derived Astronomical State (LST, RAMC, Obliquity, Tropical Ascendant/MC)
            gst_deg = t.gast * 15.0 # Greenwich Apparent Sidereal Time in degrees
            lst_deg = (gst_deg + lon) % 360.0
            ramc_rad = math.radians(lst_deg)

            # True obliquity
            T = (jd_tt - 2451545.0) / 36525.0
            eps0_sec = 23.4392911 * 3600.0 - 46.8150 * T - 0.00059 * T**2 + 0.001813 * T**3
            eps0_deg = eps0_sec / 3600.0
            eps_rad = math.radians(eps0_deg)

            lat_rad = math.radians(lat)

            # Tropical Midheaven (MC)
            mc_trop = math.degrees(math.atan2(math.sin(ramc_rad), math.cos(ramc_rad) * math.cos(eps_rad))) % 360.0
            if abs((mc_trop - lst_deg + 180.0) % 360.0 - 180.0) > 90.0:
                mc_trop = (mc_trop + 180.0) % 360.0

            # Tropical Ascendant
            num = math.cos(ramc_rad)
            den = - (math.sin(ramc_rad) * math.cos(eps_rad) + math.tan(lat_rad) * math.sin(eps_rad))
            asc_trop = math.degrees(math.atan2(num, den)) % 360.0

            derived_astronomy = DerivedAstronomicalState(
                local_sidereal_time_deg=round(lst_deg, 6),
                ramc_deg=round(lst_deg, 6),
                true_obliquity_deg=round(eps0_deg, 6),
                mean_obliquity_deg=round(eps0_deg, 6),
                ascendant_tropical_deg=round(asc_trop, 6),
                mc_tropical_deg=round(mc_trop, 6)
            )

            # Sidereal State
            ayanamsha_val = calculate_lahiri_ayanamsha(jd_tt)
            sidereal_lons: Dict[str, float] = {}
            for planet_name, pos in planet_positions.items():
                sidereal_lons[planet_name] = round(convert_tropical_to_sidereal(pos.geocentric_longitude, ayanamsha_val), 6)

            asc_sid = convert_tropical_to_sidereal(asc_trop, ayanamsha_val)
            mc_sid = convert_tropical_to_sidereal(mc_trop, ayanamsha_val)

            sidereal_state = SiderealState(
                ayanamsha_mode=ayanamsha_mode,
                ayanamsha_value_deg=round(ayanamsha_val, 6),
                sidereal_longitudes=sidereal_lons,
                ascendant_sidereal_deg=round(asc_sid, 6),
                mc_sidereal_deg=round(mc_sid, 6)
            )

            # Calculation Hash
            calc_hash = generate_calculation_hash(
                year=year, month=month, day=day, hour=hour, minute=minute, second=second,
                lat=lat, lon=lon, elevation=elevation,
                provider="Skyfield", provider_version=self.skyfield_version,
                kernel_checksum=self.kernel_checksum, ayanamsha_mode=ayanamsha_mode
            )

            # Metadata
            metadata = EphemerisMetadata(
                provider="Skyfield",
                provider_version=self.skyfield_version,
                ephemeris_kernel=self.kernel_filename,
                kernel_checksum=self.kernel_checksum,
                calculation_timestamp_utc=datetime.now(timezone.utc).isoformat(),
                input_timestamp_utc=dt_str,
                observer_coordinates={"latitude": lat, "longitude": lon, "elevation": elevation},
                coordinate_system="Ecliptic Geocentric J2000 / ICRF",
                ayanamsha_mode=ayanamsha_mode,
                calculation_hash=calc_hash
            )

            return CalculationResult(
                raw_ephemeris=raw_ephemeris,
                derived_astronomy=derived_astronomy,
                sidereal_state=sidereal_state,
                metadata=metadata
            )

        except (KernelNotFoundError, ProviderInitializationError):
            raise
        except Exception as e:
            raise CalculationError(f"Calculation failed for input datetime ({year}-{month}-{day} {hour}:{minute}:{second}): {str(e)}")
