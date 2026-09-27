class WesternEngine:
    """
    WesternEngine calculates Tropical zodiac placements, house systems,
    and major aspects (conjunction, opposition, trine, square, sextile).
    """

    ASPECTS = [
        {"name": "Conjunction", "angle": 0, "orb": 8},
        {"name": "Sextile", "angle": 60, "orb": 6},
        {"name": "Square", "angle": 90, "orb": 8},
        {"name": "Trine", "angle": 120, "orb": 8},
        {"name": "Opposition", "angle": 180, "orb": 8}
    ]

    @classmethod
    def calculate_aspects(cls, positions: dict) -> list:
        planet_names = list(positions.keys())
        aspects_found = []

        for i in range(len(planet_names)):
            for j in range(i + 1, len(planet_names)):
                p1 = planet_names[i]
                p2 = planet_names[j]
                lon1 = positions[p1]["longitude"]
                lon2 = positions[p2]["longitude"]

                diff = abs(lon1 - lon2)
                if diff > 180:
                    diff = 360 - diff

                for asp in cls.ASPECTS:
                    if abs(diff - asp["angle"]) <= asp["orb"]:
                        aspects_found.append({
                            "planet1": p1,
                            "planet2": p2,
                            "aspect": asp["name"],
                            "orb": round(abs(diff - asp["angle"]), 2)
                        })
        return aspects_found
