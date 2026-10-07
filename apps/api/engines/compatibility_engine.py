"""
Authoritative Local Vedic Ashtakoota Compatibility Matching Engine for Astrovision.
Computes exact 36-point Ashtakoota matching scores across all 8 Koota categories:
Varna (1), Vashya (2), Tara/Dina (3), Yoni (4), Graha Maitri (5), Gana (6), Bhakoot (7), Nadi (8).
Includes traditional exception/cancellation rules for Bhakoot Dosha and Nadi Dosha.
"""
from typing import Dict, List, Tuple, Any, Optional

# --- 27 NAKSHATRA METADATA TABLE ---
# Format: Nakshatra Name -> list of 4 Pada details: (Rashi_Index [1..12], Rashi_Lord, Gana, Yoni_Species, Yoni_Gender, Nadi, Varna, Vashya)
NAKSHATRA_DATA: Dict[str, Dict[str, Any]] = {
    "Ashwini": {
        "lord": "Ketu", "gana": "Deva", "yoni": "Horse", "gender": "Male", "nadi": "Adi", "varna": "Kshatriya", "vashya": "Chatushpada",
        "rashi": 1, "rashi_lord": "Mars"
    },
    "Bharani": {
        "lord": "Venus", "gana": "Manushya", "yoni": "Elephant", "gender": "Female", "nadi": "Madhya", "varna": "Kshatriya", "vashya": "Chatushpada",
        "rashi": 1, "rashi_lord": "Mars"
    },
    "Krittika": {
        "lord": "Sun", "gana": "Rakshasa", "yoni": "Sheep", "gender": "Female", "nadi": "Antya",
        "padas": {
            1: {"rashi": 1, "rashi_lord": "Mars", "varna": "Kshatriya", "vashya": "Chatushpada"},
            2: {"rashi": 2, "rashi_lord": "Venus", "varna": "Vaishya", "vashya": "Chatushpada"},
            3: {"rashi": 2, "rashi_lord": "Venus", "varna": "Vaishya", "vashya": "Chatushpada"},
            4: {"rashi": 2, "rashi_lord": "Venus", "varna": "Vaishya", "vashya": "Chatushpada"}
        }
    },
    "Rohini": {
        "lord": "Moon", "gana": "Deva", "yoni": "Serpent", "gender": "Male", "nadi": "Antya", "varna": "Vaishya", "vashya": "Chatushpada",
        "rashi": 2, "rashi_lord": "Venus"
    },
    "Mrigashira": {
        "lord": "Mars", "gana": "Deva", "yoni": "Serpent", "gender": "Female", "nadi": "Madhya",
        "padas": {
            1: {"rashi": 2, "rashi_lord": "Venus", "varna": "Vaishya", "vashya": "Chatushpada"},
            2: {"rashi": 2, "rashi_lord": "Venus", "varna": "Vaishya", "vashya": "Chatushpada"},
            3: {"rashi": 3, "rashi_lord": "Mercury", "varna": "Shudra", "vashya": "Dwipada"},
            4: {"rashi": 3, "rashi_lord": "Mercury", "varna": "Shudra", "vashya": "Dwipada"}
        }
    },
    "Ardra": {
        "lord": "Rahu", "gana": "Manushya", "yoni": "Dog", "gender": "Female", "nadi": "Adi", "varna": "Shudra", "vashya": "Dwipada",
        "rashi": 3, "rashi_lord": "Mercury"
    },
    "Punarvasu": {
        "lord": "Jupiter", "gana": "Deva", "yoni": "Cat", "gender": "Female", "nadi": "Adi",
        "padas": {
            1: {"rashi": 3, "rashi_lord": "Mercury", "varna": "Shudra", "vashya": "Dwipada"},
            2: {"rashi": 3, "rashi_lord": "Mercury", "varna": "Shudra", "vashya": "Dwipada"},
            3: {"rashi": 3, "rashi_lord": "Mercury", "varna": "Shudra", "vashya": "Dwipada"},
            4: {"rashi": 4, "rashi_lord": "Moon", "varna": "Brahmin", "vashya": "Jalachara"}
        }
    },
    "Pushya": {
        "lord": "Saturn", "gana": "Deva", "yoni": "Goat", "gender": "Female", "nadi": "Madhya", "varna": "Brahmin", "vashya": "Jalachara",
        "rashi": 4, "rashi_lord": "Moon"
    },
    "Ashlesha": {
        "lord": "Mercury", "gana": "Rakshasa", "yoni": "Cat", "gender": "Male", "nadi": "Antya", "varna": "Brahmin", "vashya": "Jalachara",
        "rashi": 4, "rashi_lord": "Moon"
    },
    "Magha": {
        "lord": "Ketu", "gana": "Rakshasa", "yoni": "Rat", "gender": "Male", "nadi": "Antya", "varna": "Kshatriya", "vashya": "Vanchara",
        "rashi": 5, "rashi_lord": "Sun"
    },
    "Purva Phalguni": {
        "lord": "Venus", "gana": "Manushya", "yoni": "Rat", "gender": "Female", "nadi": "Madhya", "varna": "Kshatriya", "vashya": "Vanchara",
        "rashi": 5, "rashi_lord": "Sun"
    },
    "Uttara Phalguni": {
        "lord": "Sun", "gana": "Manushya", "yoni": "Cow", "gender": "Male", "nadi": "Adi",
        "padas": {
            1: {"rashi": 5, "rashi_lord": "Sun", "varna": "Kshatriya", "vashya": "Vanchara"},
            2: {"rashi": 6, "rashi_lord": "Mercury", "varna": "Vaishya", "vashya": "Dwipada"},
            3: {"rashi": 6, "rashi_lord": "Mercury", "varna": "Vaishya", "vashya": "Dwipada"},
            4: {"rashi": 6, "rashi_lord": "Mercury", "varna": "Vaishya", "vashya": "Dwipada"}
        }
    },
    "Hasta": {
        "lord": "Moon", "gana": "Deva", "yoni": "Buffalo", "gender": "Female", "nadi": "Adi", "varna": "Vaishya", "vashya": "Dwipada",
        "rashi": 6, "rashi_lord": "Mercury"
    },
    "Chitra": {
        "lord": "Mars", "gana": "Rakshasa", "yoni": "Tiger", "gender": "Female", "nadi": "Madhya",
        "padas": {
            1: {"rashi": 6, "rashi_lord": "Mercury", "varna": "Vaishya", "vashya": "Dwipada"},
            2: {"rashi": 6, "rashi_lord": "Mercury", "varna": "Vaishya", "vashya": "Dwipada"},
            3: {"rashi": 7, "rashi_lord": "Venus", "varna": "Shudra", "vashya": "Dwipada"},
            4: {"rashi": 7, "rashi_lord": "Venus", "varna": "Shudra", "vashya": "Dwipada"}
        }
    },
    "Swati": {
        "lord": "Rahu", "gana": "Deva", "yoni": "Buffalo", "gender": "Male", "nadi": "Antya", "varna": "Shudra", "vashya": "Dwipada",
        "rashi": 7, "rashi_lord": "Venus"
    },
    "Vishakha": {
        "lord": "Jupiter", "gana": "Rakshasa", "yoni": "Tiger", "gender": "Male", "nadi": "Antya",
        "padas": {
            1: {"rashi": 7, "rashi_lord": "Venus", "varna": "Shudra", "vashya": "Dwipada"},
            2: {"rashi": 7, "rashi_lord": "Venus", "varna": "Shudra", "vashya": "Dwipada"},
            3: {"rashi": 7, "rashi_lord": "Venus", "varna": "Shudra", "vashya": "Dwipada"},
            4: {"rashi": 8, "rashi_lord": "Mars", "varna": "Brahmin", "vashya": "Keeta"}
        }
    },
    "Anuradha": {
        "lord": "Saturn", "gana": "Deva", "yoni": "Deer", "gender": "Female", "nadi": "Madhya", "varna": "Brahmin", "vashya": "Keeta",
        "rashi": 8, "rashi_lord": "Mars"
    },
    "Jyeshtha": {
        "lord": "Mercury", "gana": "Rakshasa", "yoni": "Deer", "gender": "Male", "nadi": "Adi", "varna": "Brahmin", "vashya": "Keeta",
        "rashi": 8, "rashi_lord": "Mars"
    },
    "Mula": {
        "lord": "Ketu", "gana": "Rakshasa", "yoni": "Dog", "gender": "Male", "nadi": "Adi", "varna": "Kshatriya", "vashya": "Chatushpada",
        "rashi": 9, "rashi_lord": "Jupiter"
    },
    "Purva Ashadha": {
        "lord": "Venus", "gana": "Manushya", "yoni": "Monkey", "gender": "Male", "nadi": "Madhya", "varna": "Kshatriya", "vashya": "Dwipada",
        "rashi": 9, "rashi_lord": "Jupiter"
    },
    "Uttara Ashadha": {
        "lord": "Sun", "gana": "Manushya", "yoni": "Mongoose", "gender": "Male", "nadi": "Antya",
        "padas": {
            1: {"rashi": 9, "rashi_lord": "Jupiter", "varna": "Kshatriya", "vashya": "Dwipada"},
            2: {"rashi": 10, "rashi_lord": "Saturn", "varna": "Vaishya", "vashya": "Jalachara"},
            3: {"rashi": 10, "rashi_lord": "Saturn", "varna": "Vaishya", "vashya": "Jalachara"},
            4: {"rashi": 10, "rashi_lord": "Saturn", "varna": "Vaishya", "vashya": "Jalachara"}
        }
    },
    "Shravana": {
        "lord": "Moon", "gana": "Deva", "yoni": "Monkey", "gender": "Female", "nadi": "Antya", "varna": "Vaishya", "vashya": "Jalachara",
        "rashi": 10, "rashi_lord": "Saturn"
    },
    "Dhanishta": {
        "lord": "Mars", "gana": "Rakshasa", "yoni": "Lion", "gender": "Female", "nadi": "Madhya",
        "padas": {
            1: {"rashi": 10, "rashi_lord": "Saturn", "varna": "Vaishya", "vashya": "Jalachara"},
            2: {"rashi": 10, "rashi_lord": "Saturn", "varna": "Vaishya", "vashya": "Jalachara"},
            3: {"rashi": 11, "rashi_lord": "Saturn", "varna": "Shudra", "vashya": "Dwipada"},
            4: {"rashi": 11, "rashi_lord": "Saturn", "varna": "Shudra", "vashya": "Dwipada"}
        }
    },
    "Shatabhisha": {
        "lord": "Rahu", "gana": "Rakshasa", "yoni": "Horse", "gender": "Female", "nadi": "Adi", "varna": "Shudra", "vashya": "Dwipada",
        "rashi": 11, "rashi_lord": "Saturn"
    },
    "Purva Bhadrapada": {
        "lord": "Jupiter", "gana": "Manushya", "yoni": "Lion", "gender": "Male", "nadi": "Adi",
        "padas": {
            1: {"rashi": 11, "rashi_lord": "Saturn", "varna": "Shudra", "vashya": "Dwipada"},
            2: {"rashi": 11, "rashi_lord": "Saturn", "varna": "Shudra", "vashya": "Dwipada"},
            3: {"rashi": 11, "rashi_lord": "Saturn", "varna": "Shudra", "vashya": "Dwipada"},
            4: {"rashi": 12, "rashi_lord": "Jupiter", "varna": "Brahmin", "vashya": "Jalachara"}
        }
    },
    "Uttara Bhadrapada": {
        "lord": "Saturn", "gana": "Manushya", "yoni": "Cow", "gender": "Female", "nadi": "Madhya", "varna": "Brahmin", "vashya": "Jalachara",
        "rashi": 12, "rashi_lord": "Jupiter"
    },
    "Revati": {
        "lord": "Mercury", "gana": "Deva", "yoni": "Elephant", "gender": "Male", "nadi": "Antya", "varna": "Brahmin", "vashya": "Jalachara",
        "rashi": 12, "rashi_lord": "Jupiter"
    }
}

# Ordered list of 27 Nakshatras for index lookups
NAKSHATRA_ORDER = list(NAKSHATRA_DATA.keys())

# Sworn Enemy Yoni Pairs (0 score)
SWORN_ENEMY_YONIS = {
    frozenset(["Horse", "Buffalo"]),
    frozenset(["Elephant", "Lion"]),
    frozenset(["Sheep", "Monkey"]),
    frozenset(["Serpent", "Mongoose"]),
    frozenset(["Dog", "Deer"]),
    frozenset(["Cat", "Rat"]),
    frozenset(["Tiger", "Cow"])
}

# Planetary Friendship Matrix for Moon Rashi Lords
GRAHA_MAITRI_MATRIX = {
    ("Sun", "Sun"): 5.0, ("Sun", "Moon"): 5.0, ("Sun", "Mars"): 5.0, ("Sun", "Jupiter"): 5.0, ("Sun", "Mercury"): 4.0, ("Sun", "Venus"): 0.0, ("Sun", "Saturn"): 0.0,
    ("Moon", "Moon"): 5.0, ("Moon", "Mars": 4.0, ("Moon", "Jupiter"): 4.0, ("Moon", "Mercury"): 5.0, ("Moon", "Venus"): 0.5, ("Moon", "Saturn"): 0.5,
    ("Mars", "Mars"): 5.0, ("Mars", "Jupiter"): 5.0, ("Mars", "Mercury"): 0.5, ("Mars", "Venus"): 3.0, ("Mars", "Saturn"): 0.5,
    ("Mercury", "Mercury"): 5.0, ("Mercury", "Venus"): 5.0, ("Mercury", "Jupiter"): 4.0, ("Mercury", "Saturn"): 4.0,
    ("Jupiter", "Jupiter"): 5.0, ("Jupiter", "Venus"): 0.5, ("Jupiter", "Saturn"): 3.0,
    ("Venus", "Venus"): 5.0, ("Venus", "Saturn"): 5.0,
    ("Saturn", "Saturn"): 5.0
}

VARNA_GRADES = {"Brahmin": 4, "Kshatriya": 3, "Vaishya": 2, "Shudra": 1}

class CompatibilityEngine:
    """
    Authoritative Local Vedic Ashtakoota Compatibility Engine.
    """

    @classmethod
    def parse_nakshatra(cls, input_str: str, pada_override: Optional[int] = None) -> Tuple[str, int, Dict[str, Any]]:
        if not input_str or not isinstance(input_str, str):
            raise ValueError(f"Invalid Nakshatra input: '{input_str}'. Must be a valid string.")

        clean_str = input_str.strip()
        pada = pada_override or 1

        # Check hyphenated format e.g. "Krittika-1"
        if "-" in clean_str:
            parts = clean_str.split("-")
            clean_str = parts[0].strip()
            if len(parts) > 1 and parts[1].strip().isdigit():
                pada = int(parts[1].strip())

        # Match Nakshatra name
        matched_name = next((n for n in NAKSHATRA_ORDER if n.lower() == clean_str.lower()), None)
        if not matched_name:
            raise ValueError(
                f"Unknown Nakshatra '{input_str}'. Valid 27 Nakshatras: {NAKSHATRA_ORDER}"
            )

        if not (1 <= pada <= 4):
            raise ValueError(f"Nakshatra Pada must be in range [1, 4]. Got {pada}.")

        base_data = NAKSHATRA_DATA[matched_name]
        parsed_info = {
            "nakshatra_name": matched_name,
            "nakshatra_index": NAKSHATRA_ORDER.index(matched_name) + 1,
            "pada": pada,
            "lord": base_data["lord"],
            "gana": base_data["gana"],
            "yoni": base_data["yoni"],
            "gender": base_data.get("gender", "Female"),
            "nadi": base_data["nadi"]
        }

        if "padas" in base_data and pada in base_data["padas"]:
            p_info = base_data["padas"][pada]
            parsed_info["rashi"] = p_info["rashi"]
            parsed_info["rashi_lord"] = p_info["rashi_lord"]
            parsed_info["varna"] = p_info["varna"]
            parsed_info["vashya"] = p_info["vashya"]
        else:
            parsed_info["rashi"] = base_data["rashi"]
            parsed_info["rashi_lord"] = base_data["rashi_lord"]
            parsed_info["varna"] = base_data["varna"]
            parsed_info["vashya"] = base_data["vashya"]

        return matched_name, pada, parsed_info

    @classmethod
    def calculate_ashtakoota(
        cls,
        person_a_moon_nak: str,
        person_b_moon_nak: str,
        person_a_pada: Optional[Int] = None,
        person_b_pada: Optional[Int] = None
    ) -> dict:
        # Parse Boy (Person A) and Girl (Person B)
        boy_name, boy_pada, boy = cls.parse_nakshatra(person_a_moon_nak, person_a_pada)
        girl_name, girl_pada, girl = cls.parse_nakshatra(person_b_moon_nak, person_b_pada)

        kootas = {}

        # 1. VARNA KOOTA (Max = 1)
        boy_v_grade = VARNA_GRADES.get(boy["varna"], 1)
        girl_v_grade = VARNA_GRADES.get(girl["varna"], 1)
        if boy_v_grade >= girl_v_grade:
            varna_score = 1.0
            varna_desc = f"Groom ({boy['varna']}) >= Bride ({girl['varna']}) Varna grade."
        else:
            varna_score = 0.0
            varna_desc = f"Groom ({boy['varna']}) < Bride ({girl['varna']}) Varna grade."

        kootas["varna"] = {"score": varna_score, "max": 1, "description": varna_desc}

        # 2. VASHYA KOOTA (Max = 2)
        b_vash = boy["vashya"]
        g_vash = girl["vashya"]
        if b_vash == g_vash:
            vashya_score = 2.0
            vashya_desc = f"Identical Vashya category ({b_vash})."
        elif (b_vash == "Dwipada" and g_vash in ["Chatushpada", "Jalachara", "Keeta"]) or (g_vash == "Dwipada" and b_vash in ["Chatushpada", "Jalachara", "Keeta"]):
            vashya_score = 1.0
            vashya_desc = f"Compatible Vashya pair ({b_vash} & {g_vash})."
        elif (b_vash == "Chatushpada" and g_vash == "Vanchara") or (g_vash == "Chatushpada" and b_vash == "Vanchara"):
            vashya_score = 0.5
            vashya_desc = f"Neutral Vashya pair ({b_vash} & {g_vash})."
        else:
            vashya_score = 0.0
            vashya_desc = f"Incompatible Vashya pair ({b_vash} & {g_vash})."

        kootas["vashya"] = {"score": vashya_score, "max": 2, "description": vashya_desc}

        # 3. TARA / DINA KOOTA (Max = 3)
        b_nak_idx = boy["nakshatra_index"]
        g_nak_idx = girl["nakshatra_index"]

        tara_bg = (b_nak_idx - g_nak_idx + 27) % 9
        if tara_bg == 0: tara_bg = 9

        tara_gb = (g_nak_idx - b_nak_idx + 27) % 9
        if tara_gb == 0: tara_gb = 9

        bg_auspicious = tara_bg in [2, 4, 6, 8, 9]
        gb_auspicious = tara_gb in [2, 4, 6, 8, 9]

        if bg_auspicious and gb_auspicious:
            tara_score = 3.0
            tara_desc = f"Mutual auspicious Taras ({tara_bg} & {tara_gb})."
        elif bg_auspicious or gb_auspicious:
            tara_score = 1.5
            tara_desc = f"Partially auspicious Taras ({tara_bg} & {tara_gb})."
        else:
            tara_score = 0.0
            tara_desc = f"Inauspicious Taras ({tara_bg} & {tara_gb})."

        kootas["tara"] = {"score": tara_score, "max": 3, "description": tara_desc}

        # 4. YONI KOOTA (Max = 4)
        b_yoni = boy["yoni"]
        g_yoni = girl["yoni"]
        yoni_pair = frozenset([b_yoni, g_yoni])

        if yoni_pair in SWORN_ENEMY_YONIS:
            yoni_score = 0.0
            yoni_desc = f"Sworn enemy Yonis ({b_yoni} & {g_yoni})."
        elif b_yoni == g_yoni:
            if boy["gender"] != girl["gender"]:
                yoni_score = 4.0
                yoni_desc = f"Identical Yoni species ({b_yoni}) with opposite genders."
            else:
                yoni_score = 3.0
                yoni_desc = f"Identical Yoni species ({b_yoni}) with same gender."
        else:
            yoni_score = 2.0
            yoni_desc = f"Compatible Yoni species ({b_yoni} & {g_yoni})."

        kootas["yoni"] = {"score": yoni_score, "max": 4, "description": yoni_desc}

        # 5. GRAHA MAITRI KOOTA (Max = 5)
        b_lord = boy["rashi_lord"]
        g_lord = girl["rashi_lord"]

        pair1 = (b_lord, g_lord)
        pair2 = (g_lord, b_lord)

        if pair1 in GRAHA_MAITRI_MATRIX:
            gm_score = GRAHA_MAITRI_MATRIX[pair1]
        elif pair2 in GRAHA_MAITRI_MATRIX:
            gm_score = GRAHA_MAITRI_MATRIX[pair2]
        else:
            gm_score = 1.0

        kootas["graha_maitri"] = {
            "score": gm_score,
            "max": 5,
            "description": f"Moon Rashi lords ({b_lord} & {g_lord}) friendship score: {gm_score}/5."
        }

        # 6. GANA KOOTA (Max = 6)
        b_gana = boy["gana"]
        g_gana = girl["gana"]

        if b_gana == g_gana:
            gana_score = 6.0
            gana_desc = f"Identical Gana temperament ({b_gana})."
        elif (b_gana == "Deva" and g_gana == "Manushya") or (b_gana == "Manushya" and g_gana == "Deva"):
            gana_score = 6.0
            gana_desc = f"Compatible Deva & Manushya Gana pairing."
        elif b_gana == "Deva" and g_gana == "Rakshasa":
            gana_score = 1.0
            gana_desc = f"Deva groom and Rakshasa bride Gana friction."
        else:
            gana_score = 0.0
            gana_desc = f"Incompatible Gana pairing ({b_gana} & {g_gana})."

        kootas["gana"] = {"score": gana_score, "max": 6, "description": gana_desc}

        # 7. BHAKOOT KOOTA (Max = 7)
        b_rashi = boy["rashi"]
        g_rashi = girl["rashi"]

        dist_bg = (b_rashi - g_rashi) % 12
        if dist_bg == 0: dist_bg = 12

        dist_gb = (g_rashi - b_rashi) % 12
        if dist_gb == 0: dist_gb = 12

        is_bhakoot_dosha = dist_bg in [2, 6, 8, 12] or dist_gb in [2, 6, 8, 12]

        # Bhakoot Cancellation exceptions
        bhakoot_cancelled = False
        if is_bhakoot_dosha:
            # Exception: Same lord or mutual friends
            if b_lord == g_lord or gm_score >= 4.0:
                bhakoot_cancelled = True

        if not is_bhakoot_dosha or bhakoot_cancelled:
            bhakoot_score = 7.0
            b_status = "Cancelled Bhakoot Dosha (7/7)" if bhakoot_cancelled else "Favorable Bhakoot (7/7)"
            bhakoot_desc = f"{b_status}: Rashi positions ({b_rashi} & {g_rashi})."
        else:
            bhakoot_score = 0.0
            bhakoot_desc = f"Bhakoot Dosha (0/7): Inauspicious {dist_bg}/{dist_gb} Rashi relationship."

        kootas["bhakoot"] = {"score": bhakoot_score, "max": 7, "description": bhakoot_desc}

        # 8. NADI KOOTA (Max = 8)
        b_nadi = boy["nadi"]
        g_nadi = girl["nadi"]

        is_nadi_dosha = (b_nadi == g_nadi)

        # Nadi Cancellation exceptions
        nadi_cancelled = False
        if is_nadi_dosha:
            # Exception 1: Same Nakshatra but different Rashis
            if boy_name == girl_name and b_rashi != g_rashi:
                nadi_cancelled = True
            # Exception 2: Same Rashi but different Nakshatras with friendly lords
            elif b_rashi == g_rashi and boy_name != girl_name and (b_lord == g_lord or gm_score >= 4.0):
                nadi_cancelled = True
            # Exception 3: Same Nakshatra but different Padas
            elif boy_name == girl_name and boy_pada != girl_pada:
                nadi_cancelled = True

        if not is_nadi_dosha or nadi_cancelled:
            nadi_score = 8.0
            n_status = "Cancelled Nadi Dosha (8/8)" if nadi_cancelled else "Favorable Nadi (8/8)"
            nadi_desc = f"{n_status}: Groom Nadi ({b_nadi}), Bride Nadi ({g_nadi})."
        else:
            nadi_score = 0.0
            nadi_desc = f"Nadi Dosha (0/8): Both Groom and Bride have {b_nadi} Nadi."

        kootas["nadi"] = {"score": nadi_score, "max": 8, "description": nadi_desc}

        # Totals
        total_score = sum(k["score"] for k in kootas.values())
        max_score = sum(k["max"] for k in kootas.values())
        percentage = round((total_score / max_score) * 100.0, 1)

        # Dynamic Recommendation
        if total_score >= 28.0 and not (is_nadi_dosha and not nadi_cancelled) and not (is_bhakoot_dosha and not bhakoot_cancelled):
            rec = f"Excellent match ({total_score}/36 points). Strong agreement across major Kootas."
        elif total_score >= 21.0 and not (is_nadi_dosha and not nadi_cancelled):
            rec = f"Good match ({total_score}/36 points). Favorable for marriage with general agreement."
        elif total_score >= 18.0:
            rec = f"Average match ({total_score}/36 points). Acceptable with moderate agreement."
        else:
            rec = f"Unfavorable match ({total_score}/36 points). Low agreement across key Ashtakoota factors."

        return {
            "system": "Ashtakoota Vedic Matching (36 Points)",
            "groom_nakshatra": f"{boy_name} (Pada {boy_pada})",
            "bride_nakshatra": f"{girl_name} (Pada {girl_pada})",
            "total_score": total_score,
            "max_score": max_score,
            "percentage": percentage,
            "has_nadi_dosha": is_nadi_dosha and not nadi_cancelled,
            "has_bhakoot_dosha": is_bhakoot_dosha and not bhakoot_cancelled,
            "kootas": kootas,
            "recommendation": rec
        }
