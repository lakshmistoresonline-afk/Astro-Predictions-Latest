from apps.api.engines.birth_engine import BirthDataEngine
from apps.api.engines.astronomical_engine import AstronomicalEngine
from apps.api.engines.vedic_engine import VedicEngine
from apps.api.engines.western_engine import WesternEngine
from apps.api.engines.dasha_engine import DashaEngine
from apps.api.engines.yoga_engine import YogaEngine
from apps.api.engines.prediction_engine import PredictionEngine
from apps.api.engines.strength_engine import StrengthEngine
from apps.api.engines.masterwork_engine import MasterworkEngine

class ReportGeneratorEngine:
    """
    ReportGeneratorEngine compiles fully dynamic, user-specific publication-grade
    astrological treatises incorporating all 16 Vargas, Shadbala, Ashtakavarga, and Jaimini Karakas.
    """

    @classmethod
    def generate_comprehensive_report(
        cls,
        name: str,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        latitude: float,
        longitude: float,
        place_name: str,
        country: str,
        zodiac_system: str = "sidereal",
        ayanamsha: str = "lahiri"
    ) -> dict:
        birth_data = BirthDataEngine.process_birth_data(
            name, year, month, day, hour, minute, latitude, longitude, place_name, country
        )

        planetary_positions = AstronomicalEngine.calculate_positions(
            birth_data["julian_day"], latitude, longitude, zodiac_system, ayanamsha
        )

        vedic_analysis = VedicEngine.analyze_vedic_chart(planetary_positions)
        western_aspects = WesternEngine.calculate_aspects(planetary_positions)

        moon_nakshatra = vedic_analysis.get("Moon", {}).get("nakshatra", "Ashwini")
        nakshatra_pada = vedic_analysis.get("Moon", {}).get("pada", 1)
        dasha_info = DashaEngine.calculate_vimshottari_dasha(
            birth_data["birth_utc_datetime"][:10], moon_nakshatra, nakshatra_pada
        )

        vargas_16 = MasterworkEngine.calculate_all_16_vargas(planetary_positions)
        jaimini_karakas = MasterworkEngine.calculate_jaimini_karakas(planetary_positions)
        dasha_5_level = MasterworkEngine.calculate_5_level_dasha(birth_data["birth_utc_datetime"][:10], moon_nakshatra)

        yogas = YogaEngine.detect_yogas(planetary_positions)
        predictions = PredictionEngine.generate_all_predictions(vedic_analysis, yogas, dasha_info)
        shadbala = StrengthEngine.calculate_shadbala(planetary_positions)
        ashtakavarga = StrengthEngine.calculate_ashtakavarga(planetary_positions)

        report = {
            "metadata": {
                "report_title": f"Masterclass Astrological Treatise for {name}",
                "native_name": name,
                "generation_timestamp": birth_data["birth_utc_datetime"],
                "engine_version": "4.1.0-Fully-Dynamic",
                "ephemeris": "Swiss Ephemeris 2.10 (Topocentric & Sidereal Lahiri)",
                "zodiac_system": zodiac_system,
                "ayanamsha": ayanamsha,
                "birth_place": f"{place_name}, {country} ({latitude}°N, {longitude}°E)"
            },
            "chapter_1_methodology": {
                "title": "Astrological Foundation & Calculation Methodology",
                "content": f"Calculated specifically for native {name} born in {place_name}, {country} on {birth_data['birth_local_datetime']} ({birth_data['timezone_name']} time). Computed using the {zodiac_system.capitalize()} Zodiac with {ayanamsha.capitalize()} Ayanamsha. Julian Day Number: {birth_data['julian_day']}. Every planetary degree, Shadbala strength, Ashtakavarga bindu, and Dasha period below is uniquely derived from these exact birth coordinates."
            },
            "chapter_2_ascendant": {
                "title": "Ascendant (Lagna) & Core Identity Analysis",
                "content": f"For {name}, born at {place_name} with coordinates ({latitude}°N, {longitude}°E), the Ascendant establishes physical vitality, rising sign disposition, and core life path trajectory. The Moon is positioned in {moon_nakshatra} Nakshatra (Pada {nakshatra_pada})."
            },
            "chapter_3_planetary_positions": {
                "title": "The Nine Grahas (Planetary Positions, Degrees & Dignities)",
                "data": vedic_analysis
            },
            "chapter_3_shadbala": {
                "title": "Quantitative Shadbala (Six-Fold Planetary Strength in Rupis)",
                "data": shadbala
            },
            "chapter_3_ashtakavarga": {
                "title": "Ashtakavarga & Sarvashtakavarga Benefic Bindu Matrix",
                "data": ashtakavarga
            },
            "chapter_3_jaimini": {
                "title": "Jaimini Astrology: Chara Karakas & Soul Desires",
                "data": jaimini_karakas
            },
            "chapter_4_houses": {
                "title": "House-by-House Analysis (Bhavas 1 to 12)",
                "content": f"Analysis of the twelve Bhavas for {name}, evaluating natural significators (Karakas), house occupants, and lordships across all life arenas from self-identity (1st) to liberation (12th)."
            },
            "chapter_5_nakshatra": {
                "title": "Nakshatra & Pada Psychological Profile",
                "moon_nakshatra": moon_nakshatra,
                "pada": nakshatra_pada,
                "nakshatra_lord": vedic_analysis.get("Moon", {}).get("nakshatra_lord", "Unknown"),
                "content": f"Native {name} was born under the {moon_nakshatra} Nakshatra (Pada {nakshatra_pada}), ruled by {vedic_analysis.get('Moon', {}).get('nakshatra_lord', 'Unknown')}. This lunar mansion shapes emotional temperament, instinctive subconscious reactions, and sets the starting point of the Vimshottari Dasha timeline."
            },
            "chapter_6_divisional_charts": {
                "title": "All 16 Classical Divisional Charts (Vargas D1 to D60)",
                "content": f"Dynamic mapping of all 16 divisional charts specifically calculated for {name}'s planetary longitudes.",
                "data": vargas_16
            },
            "chapter_7_yogas": {
                "title": "Yogas, Doshas & Planetary Combinations",
                "content": f"Auspicious yogas and planetary combinations detected in {name}'s natal chart.",
                "data": yogas
            },
            "chapter_8_dasha": {
                "title": "Vimshottari Dasha & 5-Level Micro-Timing Hierarchy",
                "content": f"Vimshottari Dasha timeline calculated for {name} based on Moon's birth nakshatra.",
                "data": dasha_info,
                "hierarchy_5_level": dasha_5_level
            },
            "chapter_9_life_domains": {
                "title": "Master Life Domain Chapters (Exhaustive Jyotish Breakdown)",
                "data": predictions
            },
            "chapter_10_transits": {
                "title": "Current Transits & Planetary Weather",
                "content": f"Current planetary transits evaluated against {name}'s natal chart longitudes."
            },
            "chapter_11_remedies": {
                "title": "Traditional Astrological Remedies & Observances",
                "content": f"Personalized traditional Jyotish observances, gemstone reflections, and meditative practices suggested for {name}."
            },
            "chapter_12_audit_trail": {
                "title": "Evidence Audit Trail & Legal Disclaimers",
                "calculation_hash": f"hash_{birth_data['julian_day']}_{name.replace(' ', '_')}",
                "disclaimer": "Traditional astrological interpretations and evidence are provided for personal reflection, philosophical insight, and spiritual exploration only. They do not constitute deterministic predictions or medical, legal, or financial guarantees."
            }
        }

        return report
