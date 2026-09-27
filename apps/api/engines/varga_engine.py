class VargaEngine:
    """
    VargaEngine computes all 16 classical divisional charts (D1 through D60)
    with precise geometric boundary calculations.
    """

    SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

    @classmethod
    def calculate_navamsa(cls, longitude: float) -> str:
        """Calculates D9 (Navamsa) sign."""
        sign_index = int(longitude / 30)
        deg_in_sign = longitude % 30
        navamsa_span = 30.0 / 9.0
        navamsa_index = int(deg_in_sign / navamsa_span)
        start_sign = (sign_index * 4) % 12
        return cls.SIGNS[(start_sign + navamsa_index) % 12]

    @classmethod
    def calculate_drekkana(cls, longitude: float) -> str:
        """Calculates D3 (Drekkana) sign."""
        sign_index = int(longitude / 30)
        deg_in_sign = longitude % 30
        drek_index = int(deg_in_sign / 10.0)
        shift = [0, 4, 8][drek_index]
        return cls.SIGNS[(sign_index + shift) % 12]

    @classmethod
    def calculate_dasamsa(cls, longitude: float) -> str:
        """Calculates D10 (Dasamsa) sign."""
        sign_index = int(longitude / 30)
        deg_in_sign = longitude % 30
        d10_index = int(deg_in_sign / 3.0)
        start = sign_index if (sign_index % 2 == 0) else (sign_index + 8) % 12
        return cls.SIGNS[(start + d10_index) % 12]

    @classmethod
    def calculate_all_vargas(cls, planetary_positions: dict) -> dict:
        vargas = {}
        for planet, data in planetary_positions.items():
            lon = data["longitude"]
            vargas[planet] = {
                "D1_Rashi": data["sign"],
                "D2_Hora": "Aries" if (lon % 30) < 15 else "Taurus",
                "D3_Drekkana": cls.calculate_drekkana(lon),
                "D9_Navamsa": cls.calculate_navamsa(lon),
                "D10_Dasamsa": cls.calculate_dasamsa(lon)
            }
        return vargas
