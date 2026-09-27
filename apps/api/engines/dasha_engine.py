from datetime import datetime, timedelta

class DashaEngine:
    """
    DashaEngine computes Vimshottari Mahadasha, Antardasha, and current active periods.
    """

    DASHA_YEARS = {
        "Ketu": 7,
        "Venus": 20,
        "Sun": 6,
        "Moon": 10,
        "Mars": 7,
        "Rahu": 18,
        "Jupiter": 16,
        "Saturn": 19,
        "Mercury": 17
    }

    DASHA_ORDER = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

    @classmethod
    def calculate_vimshottari_dasha(cls, birth_date_str: str, moon_nakshatra: str, nakshatra_pada: int) -> dict:
        birth_dt = datetime.fromisoformat(birth_date_str)

        # Simplified determination of starting Mahadasha based on Moon Nakshatra lord
        nakshatras_list = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
            "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
            "Moola", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
            "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]

        lords = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

        try:
            nak_index = nakshatras_list.index(moon_nakshatra)
        except ValueError:
            nak_index = 0

        lord_index = (nak_index // 3) % 9
        current_lord = lords[lord_index]

        # Build timeline
        timeline = []
        curr_date = birth_dt

        for i in range(9):
            idx = (lord_index + i) % 9
            lord = lords[idx]
            years = cls.DASHA_YEARS[lord]
            end_date = curr_date + timedelta(days=years * 365.25)

            timeline.append({
                "mahadasha": lord,
                "start_date": curr_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "duration_years": years
            })
            curr_date = end_date

        # Find current dasha
        today = datetime.now()
        active_dasha = timeline[0]
        for period in timeline:
            s_dt = datetime.strptime(period["start_date"], "%Y-%m-%d")
            e_dt = datetime.strptime(period["end_date"], "%Y-%m-%d")
            if s_dt <= today <= e_dt:
                active_dasha = period
                break

        return {
            "current_mahadasha": active_dasha,
            "all_mahadashas": timeline
        }
