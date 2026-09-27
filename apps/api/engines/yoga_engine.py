class YogaEngine:
    """
    YogaEngine evaluates traditional Vedic yogas and doshas based on strict conditions.
    """

    @staticmethod
    def detect_yogas(planetary_positions: dict) -> list:
        yogas = []

        # Check Budha Aditya Yoga (Sun and Mercury in the same sign)
        if "Sun" in planetary_positions and "Mercury" in planetary_positions:
            if planetary_positions["Sun"]["sign"] == planetary_positions["Mercury"]["sign"]:
                yogas.append({
                    "id": "budha_aditya",
                    "name": "Budha Aditya Yoga",
                    "description": "Formed by the conjunction of Sun and Mercury, bestowing intelligence and communication skills.",
                    "strength": "moderate"
                })

        # Check Gaja Kesari Yoga (Jupiter in center/kendra from Moon)
        if "Jupiter" in planetary_positions and "Moon" in planetary_positions:
            signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
            jup_sign = planetary_positions["Jupiter"]["sign"]
            moon_sign = planetary_positions["Moon"]["sign"]

            try:
                jup_idx = signs.index(jup_sign)
                moon_idx = signs.index(moon_sign)
                diff = (jup_idx - moon_idx) % 12
                if diff in [0, 3, 6, 9]: # 1st, 4th, 7th, 10th from Moon
                    yogas.append({
                        "id": "gaja_kesari",
                        "name": "Gaja Kesari Yoga",
                        "description": "Formed when Jupiter is in a Kendra from the Moon, bestowing wisdom, reputation, and success.",
                        "strength": "strong"
                    })
            except ValueError:
                pass

        return yogas
