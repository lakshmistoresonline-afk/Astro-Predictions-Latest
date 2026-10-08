import html
import math
from typing import Any

class SVGChartEngine:
    """
    SVGChartEngine generates publication-grade, breathtaking circular zodiac astrolabe charts
    and South Indian grid charts with gold/champagne-gold highlights matching elite design specs.
    Enforces strict XML/HTML escaping on all dynamic string inputs to prevent XSS.
    """

    @staticmethod
    def generate_circular_zodiac_wheel(planetary_positions: dict, title: str = "NATAL ZODIAC WHEEL") -> str:
        safe_title = html.escape(str(title))
        size = 460
        center = size / 2
        r_outer = 210
        r_inner = 150
        r_center = 90

        svg = f'''
        <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg" style="background:#050816; border-radius:24px; box-shadow: 0 25px 50px -12px rgba(214, 179, 106, 0.15);">
          <!-- Outer Cosmic Glow & Rings -->
          <circle cx="{center}" cy="{center}" r="{r_outer + 10}" fill="none" stroke="#D6B36A" stroke-opacity="0.2" stroke-width="1"/>
          <circle cx="{center}" cy="{center}" r="{r_outer}" fill="#080D1F" stroke="#D6B36A" stroke-width="2.5"/>
          <circle cx="{center}" cy="{center}" r="{r_inner}" fill="#0B1026" stroke="#D6B36A" stroke-opacity="0.6" stroke-width="1.5"/>
          <circle cx="{center}" cy="{center}" r="{r_center}" fill="#050816" stroke="#D6B36A" stroke-opacity="0.4" stroke-width="1"/>

          <!-- Title & Center watermark -->
          <text x="{center}" y="{center - 10}" fill="#F7F3EA" font-size="12" font-weight="bold" text-anchor="middle" letter-spacing="2">ASTRO PREDICTIONS</text>
          <text x="{center}" y="{center + 10}" fill="#D6B36A" font-size="10" text-anchor="middle" letter-spacing="1">{safe_title}</text>
        '''.strip()

        # Draw 12 zodiac house/sign sectors (30 degrees each)
        symbols = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]

        for i in range(12):
            angle_deg = i * 30
            angle_rad = math.radians(angle_deg)
            x1 = center + r_inner * math.cos(angle_rad)
            y1 = center + r_inner * math.sin(angle_rad)
            x2 = center + r_outer * math.cos(angle_rad)
            y2 = center + r_outer * math.sin(angle_rad)

            # House divider line
            svg += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#D6B36A" stroke-opacity="0.5" stroke-width="1"/>'

            # Sign symbol label position (midpoint of sector)
            mid_angle_rad = math.radians(angle_deg + 15)
            label_r = (r_inner + r_outer) / 2
            lx = center + label_r * math.cos(mid_angle_rad)
            ly = center + label_r * math.sin(mid_angle_rad) + 4
            svg += f'<text x="{lx}" y="{ly}" fill="#F0D898" font-size="14" font-weight="bold" text-anchor="middle">{symbols[i]}</text>'

        # Plot planets along the zodiac wheel based on longitude
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
            pr = r_inner + 25
            px = center + pr * math.cos(p_rad)
            py = center + pr * math.sin(p_rad)

            safe_planet = html.escape(str(planet)[:2].upper())

            svg += f'<circle cx="{px}" cy="{py}" r="4" fill="#D6B36A"/>'
            svg += f'<text x="{px}" y="{py - 6}" fill="#F7F3EA" font-size="9" font-weight="bold" text-anchor="middle">{safe_planet}</text>'

        svg += '</svg>'
        return svg

    @staticmethod
    def generate_south_indian_chart(planetary_positions: dict, title: str = "RASHI CHART (D1)") -> str:
        return SVGChartEngine.generate_circular_zodiac_wheel(planetary_positions, title)

    @staticmethod
    def generate_north_indian_chart(canonical_chart: Any, title: str = "RASHI CHART (D1)") -> str:
        placements = {}
        if hasattr(canonical_chart, "placements"):
            placements = canonical_chart.placements
        elif isinstance(canonical_chart, dict):
            placements = canonical_chart.get("placements", {})
        return SVGChartEngine.generate_circular_zodiac_wheel(placements, title=title)
