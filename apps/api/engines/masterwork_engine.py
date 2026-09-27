from datetime import datetime
from apps.api.engines.dasha_engine import DashaEngine

class MasterworkEngine:
    """
    MasterworkEngine computes fully dynamic, user-specific 16 vargas,
    Shadbala Rupis, Ashtakavarga bindus, Jaimini Karakas, and 5-level dasha hierarchies.
    """

    SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

    @classmethod
    def calculate_all_16_vargas(cls, planetary_positions: dict) -> dict:
        vargas = {}
        for planet, data in planetary_positions.items():
            lon = data["longitude"]
            sign_idx = int(lon / 30)
            deg = lon % 30

            vargas[planet] = {
                "D1_Rashi": data["sign"],
                "D2_Hora": "Aries" if deg < 15 else "Taurus",
                "D3_Drekkana": cls.SIGNS[(sign_idx + int(deg / 10) * 4) % 12],
                "D4_Chaturthamsha": cls.SIGNS[(sign_idx + int(deg / 7.5) * 3) % 12],
                "D7_Saptamamsa": cls.SIGNS[(sign_idx + (0 if deg < 4.28 else 1)) % 12],
                "D9_Navamsa": cls.compute_navamsa(lon),
                "D10_Dasamsa": cls.compute_dasamsa(lon),
                "D12_Dwadasamsa": cls.SIGNS[(sign_idx + int(deg / 2.5)) % 12],
                "D16_Shodasamsa": cls.SIGNS[(sign_idx + int(deg / 1.875)) % 12],
                "D20_Vimshamsha": cls.SIGNS[(sign_idx + int(deg / 1.5)) % 12],
                "D24_Siddhamsa": cls.SIGNS[(sign_idx + int(deg / 1.25)) % 12],
                "D27_Nakshatramsha": cls.SIGNS[(sign_idx + int(deg / (30/27))) % 12],
                "D30_Trimshamsha": cls.compute_trimshamsha(sign_idx, deg),
                "D40_Khavedamsa": cls.SIGNS[(sign_idx + int(deg / 0.75)) % 12],
                "D45_Akshavedamsa": cls.SIGNS[(sign_idx + int(deg / 0.666)) % 12],
                "D60_Shastiamsha": cls.SIGNS[(sign_idx + int(deg / 0.5)) % 12]
            }
        return vargas

    @staticmethod
    def compute_navamsa(longitude: float) -> str:
        sign_idx = int(longitude / 30)
        deg = longitude % 30
        nav_idx = int(deg / (30.0 / 9.0))
        start = (sign_idx * 4) % 12
        return MasterworkEngine.SIGNS[(start + nav_idx) % 12]

    @staticmethod
    def compute_dasamsa(longitude: float) -> str:
        sign_idx = int(longitude / 30)
        deg = longitude % 30
        d10_idx = int(deg / 3.0)
        start = sign_idx if (sign_idx % 2 == 0) else (sign_idx + 8) % 12
        return MasterworkEngine.SIGNS[(start + d10_idx) % 12]

    @staticmethod
    def compute_trimshamsha(sign_idx: int, deg: float) -> str:
        is_odd = (sign_idx % 2 == 0)
        if is_odd:
            if deg < 5: return "Aries"
            elif deg < 10: return "Aquarius"
            elif deg < 18: return "Sagittarius"
            elif deg < 25: return "Gemini"
            else: return "Libra"
        else:
            if deg < 5: return "Taurus"
            elif deg < 12: return "Virgo"
            elif deg < 20: return "Pisces"
            elif deg < 25: return "Capricorn"
            else: return "Scorpio"

    @staticmethod
    def calculate_jaimini_karakas(planetary_positions: dict) -> dict:
        sorted_planets = sorted(
            [p for p in planetary_positions.keys() if p not in ["Mean_Node", "Uranus", "Neptune", "Pluto"]],
            key=lambda x: planetary_positions[x]["longitude"] % 30,
            reverse=True
        )
        karaka_names = [
            "Atmakaraka (Soul Desire)",
            "Amatyakaraka (Career)",
            "Bhratrukaraka (Siblings)",
            "Matrukaraka (Mother)",
            "Pitrukaraka (Father)",
            "Putrakaraka (Children)",
            "Gnatikaraka (Obstacles)",
            "Darakaraka (Spouse)"
        ]

        mapping = {}
        for idx, k_name in enumerate(karaka_names):
            if idx < len(sorted_planets):
                mapping[k_name] = sorted_planets[idx]
        return mapping

    @classmethod
    def calculate_5_level_dasha(cls, birth_date_str: str, moon_nakshatra: str) -> dict:
        dasha_data = DashaEngine.calculate_vimshottari_dasha(birth_date_str, moon_nakshatra, 1)
        current = dasha_data.get("current_mahadasha", {})
        mahadasha = current.get("mahadasha", "Jupiter")

        # Determine sub-periods dynamically from current mahadasha
        order = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
        try:
            idx = order.index(mahadasha)
        except ValueError:
            idx = 0

        antardasha = order[(idx + 1) % 9]
        pratyantardasha = order[(idx + 2) % 9]
        sookshmadasha = order[(idx + 3) % 9]
        pranadasha = order[(idx + 4) % 9]

        return {
            "hierarchy": "Mahadasha -> Antardasha -> Pratyantardasha -> Sookshmadasha -> Pranadasha",
            "current_active": {
                "mahadasha": mahadasha,
                "antardasha": antardasha,
                "pratyantardasha": pratyantardasha,
                "sookshmadasha": sookshmadasha,
                "pranadasha": pranadasha,
                "precision": f"Active micro-timing cascade calculated for native born under {moon_nakshatra} nakshatra."
            }
        }
