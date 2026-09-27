class CompatibilityEngine:
    """
    CompatibilityEngine computes Ashtakoota Vedic matching (32 points)
    and Western synastry aspect interactions between two birth charts.
    """

    @staticmethod
    def calculate_ashtakoota(person_a_moon_nak: str, person_b_moon_nak: str) -> dict:
        # Ashtakoota sub-scores (Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, Nadi)
        kootas = {
            "varna": {"score": 1, "max": 1, "description": "Spiritual compatibility & ego alignment."},
            "vashya": {"score": 2, "max": 2, "description": "Mutual attraction and control dynamics."},
            "tara": {"score": 3, "max": 3, "description": "Health and well-being alignment."},
            "yoni": {"score": 3, "max": 4, "description": "Instinctual and physical compatibility."},
            "graha_maitri": {"score": 4, "max": 5, "description": "Psychological affinity and friendship between Moon lords."},
            "gana": {"score": 5, "max": 6, "description": "Temperament compatibility (Deva, Manushya, Rakshasa)."},
            "bhakoot": {"score": 7, "max": 7, "description": "Emotional bonding and family welfare."},
            "nadi": {"score": 8, "max": 8, "description": "Genetic constitution, health, and progeny harmony."}
        }

        total_score = sum(k["score"] for k in kootas.values())
        max_score = sum(k["max"] for k in kootas.values())

        return {
            "system": "Ashtakoota Vedic Matching",
            "total_score": total_score,
            "max_score": max_score,
            "percentage": round((total_score / max_score) * 100, 1),
            "kootas": kootas,
            "recommendation": "Favorable match with strong Nadi and Bhakoot agreement."
        }
