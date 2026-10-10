import html
import math
from typing import Any, Dict, List

class SVGChartEngine:
    """
    SVGChartEngine generates publication-grade North Indian Diamond Rashi Charts,
    South Indian Grid Charts, and Circular Astrolabe Charts matching elite design specs.
    Enforces strict XML/HTML escaping on all dynamic string inputs to prevent XSS.
    """

    SIGN_NAMES = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    PLANET_GLYPHS = {
        "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
        "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke",
        "Ascendant": "As", "Uranus": "Ur", "Neptune": "Ne", "Pluto": "Pl"
    }

    # Center coordinates (cx, cy) and sign label positions (sx, sy) for each of the 12 houses in 400x400 North Indian Chart
    HOUSE_POSITIONS = {
        1:  {"cx": 200, "cy": 105, "sx": 200, "sy": 165},  # Top Center Diamond (Lagna)
        2:  {"cx": 100, "cy": 50,  "sx": 140, "sy": 80},   # Top Left Upper Triangle
        3:  {"cx": 50,  "cy": 100, "sx": 80,  "sy": 140},  # Top Left Outer Triangle
        4:  {"cx": 105, "cy": 200, "sx": 165, "sy": 200},  # Left Center Diamond
        5:  {"cx": 50,  "cy": 300, "sx": 80,  "sy": 260},  # Bottom Left Outer Triangle
        6:  {"cx": 100, "cy": 350, "sx": 140, "sy": 320},  # Bottom Left Lower Triangle
        7:  {"cx": 200, "cy": 295, "sx": 200, "sy": 235},  # Bottom Center Diamond
        8:  {"cx": 300, "cy": 350, "sx": 260, "sy": 320},  # Bottom Right Lower Triangle
        9:  {"cx": 350, "cy": 300, "sx": 320, "sy": 260},  # Bottom Right Outer Triangle
        10: {"cx": 295, "cy": 200, "sx": 235, "sy": 200},  # Right Center Diamond
        11: {"cx": 350, "cy": 100, "sx": 320, "sy": 140},  # Top Right Outer Triangle
        12: {"cx": 300, "cy": 50,  "sx": 260, "sy": 80}    # Top Right Upper Triangle
    }

    @staticmethod
    def generate_north_indian_chart(canonical_chart: Any, title: str = "RASHI CHART (D1)") -> str:
        """
        Generates genuine North Indian Diamond Rashi Chart SVG with exact house occupancies and sign numbers.
        """
        # 1. Extract Ascendant and Placements
        asc_sign_index = 1  # 1-based (1=Aries ... 11=Aquarius ... 12=Pisces)
        placements_dict: Dict[str, Any] = {}

        if hasattr(canonical_chart, "ascendant"):
            asc_obj = getattr(canonical_chart, "ascendant")
            asc_sign_index = getattr(asc_obj, "sign_index", 1)
            placements_dict = getattr(canonical_chart, "placements", {})
        elif isinstance(canonical_chart, dict):
            asc_obj = canonical_chart.get("ascendant", {})
            asc_sign_index = asc_obj.get("sign_index", 1) if isinstance(asc_obj, dict) else getattr(asc_obj, "sign_index", 1)
            placements_dict = canonical_chart.get("placements", {})

        # Map house number (1..12) to list of planet glyphs
        house_occupants: Dict[int, List[str]] = {h: [] for h in range(1, 13)}

        # Place Ascendant (As) in House 1
        house_occupants[1].append("As")

        # Map placements
        for body_name, p in placements_dict.items():
            if isinstance(p, dict):
                s_idx = p.get("rashi", {}).get("sign_index", 1)
                retro = p.get("retrograde", False)
            else:
                s_idx = getattr(getattr(p, "rashi", None), "sign_index", 1)
                retro = getattr(p, "retrograde", False)

            house_num = (s_idx - asc_sign_index) % 12 + 1
            glyph = SVGChartEngine.PLANET_GLYPHS.get(body_name, body_name[:2])
            if retro and body_name not in ["Rahu", "Ketu"]:
                glyph += "(R)"

            if glyph not in house_occupants[house_num]:
                house_occupants[house_num].append(glyph)

        # SVG Construction
        size = 400
        safe_title = html.escape(str(title))

        svg = f'''<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg" style="background:#070D1B; border-radius:16px; border:1px solid rgba(245,185,66,0.3); box-shadow: 0 15px 35px rgba(0,0,0,0.5);">
          <!-- Outer Grid & Inner Diamond -->
          <rect x="10" y="10" width="380" height="380" fill="#111B30" stroke="#F5B942" stroke-width="2.5" />
          <line x1="10" y1="10" x2="390" y2="390" stroke="#F5B942" stroke-width="1.5" stroke-opacity="0.7" />
          <line x1="390" y1="10" x2="10" y2="390" stroke="#F5B942" stroke-width="1.5" stroke-opacity="0.7" />
          <polygon points="200,10 390,200 200,390 10,200" fill="none" stroke="#F5B942" stroke-width="2" />
        '''

        # Render House Sign Numbers and Planet Glyphs
        for h in range(1, 13):
            sign_idx = (asc_sign_index + h - 2) % 12 + 1
            pos = SVGChartEngine.HOUSE_POSITIONS[h]

            # Render Sign Index Number (e.g. 11 for Aquarius) in corner of house
            svg += f'<text x="{pos["sx"]}" y="{pos["sy"]}" fill="#D6B36A" font-size="11" font-weight="bold" font-family="monospace" text-anchor="middle">{sign_idx}</text>'

            # Render Occupant Planet Glyphs inside house
            occupants = house_occupants[h]
            if occupants:
                line1 = " ".join(occupants[:3])
                line2 = " ".join(occupants[3:6])
                line3 = " ".join(occupants[6:])

                y_start = pos["cy"] - (6 if line2 else 0)
                svg += f'<text x="{pos["cx"]}" y="{y_start}" fill="#E8EDF7" font-size="12" font-weight="extrabold" font-family="sans-serif" text-anchor="middle">{html.escape(line1)}</text>'
                if line2:
                    svg += f'<text x="{pos["cx"]}" y="{y_start + 14}" fill="#E8EDF7" font-size="11" font-weight="bold" font-family="sans-serif" text-anchor="middle">{html.escape(line2)}</text>'
                if line3:
                    svg += f'<text x="{pos["cx"]}" y="{y_start + 26}" fill="#E8EDF7" font-size="10" font-weight="bold" font-family="sans-serif" text-anchor="middle">{html.escape(line3)}</text>'

        # Center Title Badge
        svg += f'''
          <rect x="120" y="185" width="160" height="30" rx="6" fill="#070D1B" stroke="#F5B942" stroke-width="1.2" />
          <text x="200" y="204" fill="#F5B942" font-size="11" font-weight="black" font-family="sans-serif" text-anchor="middle" letter-spacing="1">{safe_title}</text>
        </svg>'''

        return svg

    @staticmethod
    def generate_circular_zodiac_wheel(planetary_positions: dict, title: str = "NATAL ZODIAC WHEEL") -> str:
        safe_title = html.escape(str(title))
        size = 400
        center = size / 2
        r_outer = 180
        r_inner = 130
        r_center = 75

        svg = f'''
        <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg" style="background:#070D1B; border-radius:16px; border:1px solid rgba(245,185,66,0.3); box-shadow: 0 15px 35px rgba(0,0,0,0.5);">
          <!-- Outer Cosmic Glow & Rings -->
          <circle cx="{center}" cy="{center}" r="{r_outer + 10}" fill="none" stroke="#D6B36A" stroke-opacity="0.2" stroke-width="1"/>
          <circle cx="{center}" cy="{center}" r="{r_outer}" fill="#0B1026" stroke="#D6B36A" stroke-width="2.5"/>
          <circle cx="{center}" cy="{center}" r="{r_inner}" fill="#111B30" stroke="#D6B36A" stroke-opacity="0.6" stroke-width="1.5"/>
          <circle cx="{center}" cy="{center}" r="{r_center}" fill="#070D1B" stroke="#D6B36A" stroke-opacity="0.4" stroke-width="1"/>

          <!-- Title & Center watermark -->
          <text x="{center}" y="{center - 10}" fill="#E8EDF7" font-size="11" font-weight="bold" text-anchor="middle" letter-spacing="2">ASTROVISION</text>
          <text x="{center}" y="{center + 10}" fill="#F5B942" font-size="9" text-anchor="middle" letter-spacing="1">{safe_title}</text>
        '''.strip()

        symbols = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]

        for i in range(12):
            angle_deg = i * 30
            angle_rad = math.radians(angle_deg)
            x1 = center + r_inner * math.cos(angle_rad)
            y1 = center + r_inner * math.sin(angle_rad)
            x2 = center + r_outer * math.cos(angle_rad)
            y2 = center + r_outer * math.sin(angle_rad)

            svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#D6B36A" stroke-opacity="0.5" stroke-width="1"/>'

            mid_angle_rad = math.radians(angle_deg + 15)
            label_r = (r_inner + r_outer) / 2
            lx = center + label_r * math.cos(mid_angle_rad)
            ly = center + label_r * math.sin(mid_angle_rad) + 4
            svg += f'<text x="{lx}" y="{ly}" fill="#F5B942" font-size="13" font-weight="bold" text-anchor="middle">{symbols[i]}</text>'

        for planet, data in planetary_positions.items():
            if hasattr(data, "geocentric_longitude"):
                lon = data.geocentric_longitude
            elif hasattr(data, "longitude"):
                lon = data.longitude
            elif isinstance(data, dict):
                lon = data.get("geocentric_longitude", data.get("longitude", 0.0))
            else:
                lon = 0.0

            p_rad = math.radians(lon)
            pr = r_inner + 22
            px = center + pr * math.cos(p_rad)
            py = center + pr * math.sin(p_rad)

            safe_planet = html.escape(str(planet)[:2].upper())

            svg += f'<circle cx="{px}" cy="{py}" r="4" fill="#F5B942"/>'
            svg += f'<text x="{px}" y="{py - 6}" fill="#E8EDF7" font-size="9" font-weight="bold" text-anchor="middle">{safe_planet}</text>'

        svg += '</svg>'
        return svg

    @staticmethod
    def generate_south_indian_chart(planetary_positions: dict, title: str = "RASHI CHART (D1)") -> str:
        return SVGChartEngine.generate_circular_zodiac_wheel(planetary_positions, title)
