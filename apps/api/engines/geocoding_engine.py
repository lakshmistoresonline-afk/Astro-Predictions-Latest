"""
Authoritative Local Geocoding & IANA Timezone Resolution Engine for Astrovision.
Provides deterministic global and India-focused location resolution with exact IANA timezone mappings.
Supports searching smaller Indian cities/towns and global metropolitan areas.
"""
import zoneinfo
from typing import List, Dict, Any, Optional

# Comprehensive Deterministic Location Database (India Tier 1/2/3 Cities & Global Metros)
CANONICAL_LOCATIONS: List[Dict[str, Any]] = [
    # --- India Cities & Towns ---
    {"place_name": "New Delhi", "country": "India", "latitude": 28.6139, "longitude": 77.2090, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Mumbai", "country": "India", "latitude": 18.9220, "longitude": 72.8347, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Bengaluru", "country": "India", "latitude": 12.9716, "longitude": 77.5946, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Chennai", "country": "India", "latitude": 13.0827, "longitude": 80.2707, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Kolkata", "country": "India", "latitude": 22.5726, "longitude": 88.3639, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Hyderabad", "country": "India", "latitude": 17.3850, "longitude": 78.4867, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Ahmedabad", "country": "India", "latitude": 23.0225, "longitude": 72.5714, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Pune", "country": "India", "latitude": 18.5204, "longitude": 73.8567, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Jaipur", "country": "India", "latitude": 26.9124, "longitude": 75.7873, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Lucknow", "country": "India", "latitude": 26.8467, "longitude": 80.9462, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Varanasi", "country": "India", "latitude": 25.3176, "longitude": 82.9739, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Coimbatore", "country": "India", "latitude": 11.0168, "longitude": 76.9558, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Kochi", "country": "India", "latitude": 9.9312, "longitude": 76.2673, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Palakkad", "country": "India", "latitude": 10.7867, "longitude": 76.6548, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Madurai", "country": "India", "latitude": 9.9252, "longitude": 78.1198, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Mysuru", "country": "India", "latitude": 12.2958, "longitude": 76.6394, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Surat", "country": "India", "latitude": 21.1702, "longitude": 72.8311, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Indore", "country": "India", "latitude": 22.7196, "longitude": 75.8577, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Nagpur", "country": "India", "latitude": 21.1458, "longitude": 79.0882, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Visakhapatnam", "country": "India", "latitude": 17.6868, "longitude": 83.2185, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Bhubaneswar", "country": "India", "latitude": 20.2961, "longitude": 85.8245, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Patna", "country": "India", "latitude": 25.5941, "longitude": 85.1376, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Guwahati", "country": "India", "latitude": 26.1445, "longitude": 91.7362, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Chandigarh", "country": "India", "latitude": 30.7333, "longitude": 76.7794, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Thiruvananthapuram", "country": "India", "latitude": 8.5241, "longitude": 76.9366, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Thrissur", "country": "India", "latitude": 10.5276, "longitude": 76.2144, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Kozhikode", "country": "India", "latitude": 11.2588, "longitude": 75.7804, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Tiruchirappalli", "country": "India", "latitude": 10.7905, "longitude": 78.7047, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Salem", "country": "India", "latitude": 11.6643, "longitude": 78.1460, "timezone_str": "Asia/Kolkata"},
    {"place_name": "Amritsar", "country": "India", "latitude": 31.6340, "longitude": 74.8723, "timezone_str": "Asia/Kolkata"},

    # --- Global International Cities ---
    {"place_name": "London", "country": "United Kingdom", "latitude": 51.5074, "longitude": -0.1278, "timezone_str": "Europe/London"},
    {"place_name": "New York", "country": "United States", "latitude": 40.7128, "longitude": -74.0060, "timezone_str": "America/New_York"},
    {"place_name": "Los Angeles", "country": "United States", "latitude": 34.0522, "longitude": -118.2437, "timezone_str": "America/Los_Angeles"},
    {"place_name": "Chicago", "country": "United States", "latitude": 41.8781, "longitude": -87.6298, "timezone_str": "America/Chicago"},
    {"place_name": "San Francisco", "country": "United States", "latitude": 37.7749, "longitude": -122.4194, "timezone_str": "America/Los_Angeles"},
    {"place_name": "Tokyo", "country": "Japan", "latitude": 35.6762, "longitude": 139.6503, "timezone_str": "Asia/Tokyo"},
    {"place_name": "Sydney", "country": "Australia", "latitude": -33.8688, "longitude": 151.2093, "timezone_str": "Australia/Sydney"},
    {"place_name": "Melbourne", "country": "Australia", "latitude": -37.8136, "longitude": 144.9631, "timezone_str": "Australia/Melbourne"},
    {"place_name": "Paris", "country": "France", "latitude": 48.8566, "longitude": 2.3522, "timezone_str": "Europe/Paris"},
    {"place_name": "Berlin", "country": "Germany", "latitude": 52.5200, "longitude": 13.4050, "timezone_str": "Europe/Berlin"},
    {"place_name": "Dubai", "country": "United Arab Emirates", "latitude": 25.2048, "longitude": 55.2708, "timezone_str": "Asia/Dubai"},
    {"place_name": "Singapore", "country": "Singapore", "latitude": 1.3521, "longitude": 103.8198, "timezone_str": "Asia/Singapore"},
    {"place_name": "Toronto", "country": "Canada", "latitude": 43.6532, "longitude": -79.3832, "timezone_str": "America/Toronto"},
    {"place_name": "Vancouver", "country": "Canada", "latitude": 49.2827, "longitude": -123.1207, "timezone_str": "America/Vancouver"},
    {"place_name": "Auckland", "country": "New Zealand", "latitude": -36.8485, "longitude": 174.7633, "timezone_str": "Pacific/Auckland"},
    {"place_name": "Zurich", "country": "Switzerland", "latitude": 47.3769, "longitude": 8.5417, "timezone_str": "Europe/Zurich"},
    {"place_name": "Rome", "country": "Italy", "latitude": 41.9028, "longitude": 12.4964, "timezone_str": "Europe/Rome"},
    {"place_name": "Cairo", "country": "Egypt", "latitude": 30.0444, "longitude": 31.2357, "timezone_str": "Africa/Cairo"},
    {"place_name": "Johannesburg", "country": "South Africa", "latitude": -26.2041, "longitude": 28.0473, "timezone_str": "Africa/Johannesburg"},
    {"place_name": "São Paulo", "country": "Brazil", "latitude": -23.5505, "longitude": -46.6333, "timezone_str": "America/Sao_Paulo"}
]

class GeocodingEngine:
    """
    GeocodingEngine resolves place names to canonical coordinates & IANA timezones.
    """

    @classmethod
    def search_location(cls, query: str) -> List[Dict[str, Any]]:
        """
        Sub-string / fuzzy search matching place name or country.
        Returns matching canonical location objects.
        """
        if not query or not isinstance(query, str) or not query.strip():
            return []

        clean_q = query.strip().lower()
        matches = []

        for loc in CANONICAL_LOCATIONS:
            p_name = loc["place_name"].lower()
            country = loc["country"].lower()
            if clean_q in p_name or clean_q in country:
                matches.append(loc)

        return matches

    @classmethod
    def validate_coordinates_and_timezone(cls, lat: float, lon: float, tz_str: str) -> bool:
        """
        Validates latitude [-90.0, 90.0], longitude [-180.0, 180.0], and IANA timezone string.
        """
        if not (-90.0 <= lat <= 90.0):
            return False
        if not (-180.0 <= lon <= 180.0):
            return False
        try:
            zoneinfo.ZoneInfo(tz_str)
            return True
        except Exception:
            return False
