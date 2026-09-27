class VedicEngine:
    """
    VedicEngine calculates Sidereal charts, Rashis, Nakshatras, Padas,
    Bhavas (Houses), and Planetary Dignities (Exaltation, Debilitation, Own Sign).
    """

    NAKSHATRAS = [
        "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
        "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
        "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
        "Moola", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
        "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]

    EXALTATIONS = {
        "Sun": ("Aries", 10),
        "Moon": ("Taurus", 3),
        "Mercury": ("Virgo", 15),
        "Venus": ("Pisces", 27),
        "Mars": ("Capricorn", 28),
        "Jupiter": ("Cancer", 5),
        "Saturn": ("Libra", 20)
    }

    DEBILITATIONS = {
        "Sun": ("Libra", 10),
        "Moon": ("Scorpio", 3),
        "Mercury": ("Pisces", 15),
        "Venus": ("Virgo", 27),
        "Mars": ("Cancer", 28),
        "Jupiter": ("Capricorn", 5),
        "Saturn": ("Aries", 20)
    }

    @classmethod
    def get_nakshatra_info(cls, longitude: float) -> dict:
        nak_span = 360.0 / 27.0  # 13 degrees 20 minutes (13.3333...)
        nak_index = int(longitude / nak_span)
        deg_in_nak = longitude % nak_span
        pada_span = nak_span / 4.0  # 3 degrees 20 minutes
        pada = int(deg_in_nak / pada_span) + 1

        return {
            "nakshatra": cls.NAKSHATRAS[nak_index % 27],
            "pada": pada,
            "nakshatra_lord": cls.get_nakshatra_lord(nak_index % 27)
        }

    @staticmethod
    def get_nakshatra_lord(index: int) -> str:
        lords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
        return lords[index % 9]

    @classmethod
    def get_planetary_dignity(cls, planet: str, sign: str) -> str:
        if planet in cls.EXALTATIONS and cls.EXALTATIONS[planet][0] == sign:
            return "Exalted"
        if planet in cls.DEBILITATIONS and cls.DEBILITATIONS[planet][0] == sign:
            return "Debilitated"
        return "Neutral"

    @classmethod
    def analyze_vedic_chart(cls, planetary_positions: dict) -> dict:
        vedic_data = {}
        for planet, data in planetary_positions.items():
            lon = data["longitude"]
            nak_info = cls.get_nakshatra_info(lon)
            dignity = cls.get_planetary_dignity(planet, data["sign"])

            vedic_data[planet] = {
                **data,
                **nak_info,
                "dignity": dignity
            }
        return vedic_data
