"""
Cryptographic Deterministic Calculation Hash for Astrovision.
Uses SHA-256 to produce an immutable, audit-ready digest of calculation inputs and configuration.
"""
import hashlib
import json

def generate_calculation_hash(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    second: int,
    lat: float,
    lon: float,
    elevation: float,
    provider: str,
    provider_version: str,
    kernel_checksum: str,
    ayanamsha_mode: str = "Lahiri",
    house_system: str = "Placidus",
    node_model: str = "Mean"
) -> str:
    """
    Generates a deterministic SHA-256 hex digest for a set of normalized astronomical inputs.
    Never uses Python's built-in non-deterministic hash().
    """
    payload = {
        "datetime_utc": f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}Z",
        "observer": {
            "latitude": round(lat, 6),
            "longitude": round(lon, 6),
            "elevation": round(elevation, 2)
        },
        "configuration": {
            "provider": provider,
            "provider_version": provider_version,
            "kernel_checksum": kernel_checksum,
            "ayanamsha_mode": ayanamsha_mode,
            "house_system": house_system,
            "node_model": node_model
        }
    }

    canonical_json = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
