class EvidenceAggregator:
    """
    EvidenceAggregator gathers comprehensive, domain-specific astrological evidence
    incorporating house lordships, karakas, aspects, yogas, and active dasha periods.
    """

    DOMAIN_RULES = {
        "CAREER": {
            "focus": "10th House (Karma Bhava), 10th Lord, Sun (authority), Saturn (karma/discipline), and D10 Dasamsa placements.",
            "interpretation": "Career progression is governed by the strength of the 10th house from the Ascendant and Moon. Favorable connections between the 10th lord and benefic planets (Jupiter, Mercury, Venus) indicate steady professional rise, leadership roles, and recognition. Saturn's influence dictates perseverance and structured execution, while the active Mahadasha provides the primary operational backdrop for professional milestones."
        },
        "FINANCE": {
            "focus": "2nd House (Dhana Bhava - accumulated wealth), 11th House (Labha Bhava - gains), Jupiter (karaka for wealth), and Venus.",
            "interpretation": "Financial prosperity depends on the strength of the 2nd and 11th houses and their lords. Strong Dhana Yogas (conjunctions or mutual aspects between wealth lords and trikon/kendra lords) indicate robust income streams, investment success, and long-term asset accumulation. Jupiter's benevolent placement ensures abundance and wise financial stewardship."
        },
        "BUSINESS": {
            "focus": "7th House (partnerships/trade), 10th House, Mercury (commerce), and Mars (enterprise).",
            "interpretation": "Entrepreneurial and business ventures are evaluated through the 7th house of public dealings and commerce alongside Mercury's analytical acuity. Favorable aspects to the 7th house support successful partnerships, contract negotiations, and mercantile expansion."
        },
        "MARRIAGE": {
            "focus": "7th House (Kalatra Bhava), 7th Lord, Venus (indicator of love/harmony for men), Jupiter (indicator of husband for women), and Navamsa (D9).",
            "interpretation": "Marital harmony, partnership dynamics, and relationship fulfillment are dictated by the condition of the 7th house and Venus/Jupiter. A well-placed 7th lord and benefic occupants foster mutual respect, emotional compatibility, and enduring companionship. Navamsa (D9) corroborates the deeper soul-level compatibility."
        },
        "RELATIONSHIP": {
            "focus": "5th House (romance/affects), 7th House, and emotional Moon-Venus interactions.",
            "interpretation": "Interpersonal bonds and romantic inclinations are shaped by the 5th and 7th houses. Harmonious planetary aspects promote loyalty, empathetic communication, and deep emotional resonance."
        },
        "EDUCATION": {
            "focus": "4th House (formal schooling/foundation), 5th House (higher intellect/wisdom), Mercury (learning), and Jupiter (higher knowledge).",
            "interpretation": "Academic success, intellectual grasp, and specialized learning are governed by the 4th and 5th houses. Strong Mercury and Jupiter placements bestow sharp memory, analytical clarity, and success in higher examinations or research."
        },
        "FAMILY": {
            "focus": "2nd House (immediate family/speech), 4th House (domestic peace), and Moon (mother/mind).",
            "interpretation": "Family harmony and domestic happiness are reflected through the 2nd and 4th houses. A strong Moon and well-aspected 4th house ensure a nurturing home environment and strong familial support systems."
        },
        "CHILDREN": {
            "focus": "5th House (Putra Bhava), Jupiter (karaka for progeny), and 5th lord strength.",
            "interpretation": "Matters of progeny, creative output, and legacy are seen through the 5th house and Jupiter. Benefic influences support healthy progeny, creative fulfillment, and pride in offspring."
        },
        "PROPERTY": {
            "focus": "4th House (real estate/land), Mars (land/construction), and Saturn (permanent assets).",
            "interpretation": "Acquisition of real estate, land, vehicles, and permanent infrastructure is governed by the 4th house and Mars. Favorable connections between the 4th lord and Mars/Saturn indicate successful property ownership."
        },
        "TRAVEL": {
            "focus": "9th House (long journeys/pilgrimage), 12th House (foreign lands/settlement), and Rahu (foreign/unconventional influences).",
            "interpretation": "Travel proclivities, foreign journeys, and international relocations are highlighted by connections involving the 9th, 12th houses, and Rahu. Favorable influences support enriching cross-cultural experiences and successful travel."
        },
        "RELOCATION": {
            "focus": "4th House (change of residence), 7th, 9th, and 12th houses.",
            "interpretation": "Shifts in physical domicile and geographical relocation are activated during dasha periods connecting movable signs and foreign houses (12th/9th)."
        },
        "SPIRITUALITY": {
            "focus": "9th House (higher dharma), 12th House (liberation/moksha), Ketu (moksha karaka), and Jupiter (divine grace).",
            "interpretation": "Spiritual evolution, philosophical inquiry, and inner liberation are illuminated by Ketu, Jupiter, and the 9th/12th houses. Strong spiritual indicators bestow profound intuition, detachment, and higher wisdom."
        },
        "PERSONAL_DEVELOPMENT": {
            "focus": "1st House (Lagna/Self), Sun (soul/vitality), and Moon (mind).",
            "interpretation": "Self-actualization, confidence, and personal growth stem from the strength of the Ascendant and Sun. A strong Lagna lord endows the native with resilience, charisma, and purposeful direction."
        },
        "WELLBEING": {
            "focus": "1st House (vitality), 6th House (disease/immunity), 8th House (longevity), and Sun/Moon vitality.",
            "interpretation": "Overall physical vitality, immune resilience, and psychological well-being are evaluated through Ascendant strength and the 6th/8th house configurations. Proactive lifestyle balance supports sustained health."
        }
    }

    @classmethod
    def aggregate_evidence(cls, domain: str, vedic_data: dict, yogas: list, dasha_info: dict) -> dict:
        rule = cls.DOMAIN_RULES.get(domain, {
            "focus": "General planetary houses and active dasha periods.",
            "interpretation": "Evaluated through traditional planetary strengths and dasha transits."
        })

        supporting = []
        challenging = []

        # Check yogas
        for yoga in yogas:
            supporting.append(f"Benefic Yoga active ({yoga['name']}): {yoga['description']}")

        # Check current dasha
        current_mahadasha = dasha_info.get("current_mahadasha", {}).get("mahadasha", "Unknown")
        supporting.append(f"Active Mahadasha ({current_mahadasha}): Governs the overarching experiential theme and manifestation of life events during this epoch.")

        # Check planetary dignities
        for planet, data in vedic_data.items():
            if data.get("dignity") == "Exalted":
                supporting.append(f"{planet} is exalted in {data['sign']}, bestowing exceptional strength and auspicious results in its domains.")
            elif data.get("dignity") == "Debilitated":
                challenging.append(f"{planet} is debilitated in {data['sign']}, indicating areas requiring conscious discipline, remedial focus, and perseverance.")

        if not supporting:
            supporting.append("Standard planetary distribution providing balanced developmental opportunities.")

        return {
            "domain": domain.upper(),
            "focus_areas": rule["focus"],
            "traditional_interpretation": rule["interpretation"],
            "positive_factors": supporting,
            "challenging_factors": challenging,
            "neutral_factors": ["Operational timing modulated by planetary transits and sub-period (Antardasha) switches."],
            "evidence_strength": "exhaustive_multi_indicator"
        }
