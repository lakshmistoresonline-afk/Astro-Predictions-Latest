"""
Cryptographic SHA-256 Hash Generation for Vimshottari Dasha Engine.
"""
import hashlib
import json

def generate_dasha_calculation_hash(
    birth_utc_iso: str,
    moon_sidereal_lon: float,
    astronomy_state_hash: str,
    dasha_convention: str = "Parashari Vimshottari 120Y",
    time_convention: str = "365.25 d/yr"
) -> str:
    """Generates deterministic SHA-256 digest for Dasha calculation inputs."""
    payload = {
        "birth_utc_iso": birth_utc_iso,
        "moon_sidereal_lon": round(moon_sidereal_lon, 6),
        "astronomy_state_hash": astronomy_state_hash,
        "dasha_convention": dasha_convention,
        "time_convention": time_convention
    }
    canonical_json = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(canonical_json.encode("utf-8")).hexdigest()
