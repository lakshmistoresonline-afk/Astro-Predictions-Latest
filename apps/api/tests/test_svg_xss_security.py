"""
Test Suite for SVG XSS Hardening & HTML/XML Escaping.
"""
import pytest
from apps.api.engines.svg_chart_engine import SVGChartEngine

def test_svg_chart_engine_escapes_xss_payloads():
    """Verifies that malicious script tags in chart titles and planet names are escaped in generated SVG."""
    xss_title = "<script>alert('XSS_TITLE')</script>"
    xss_planet = "<img src=x onerror=alert('XSS_PLANET')>"

    planetary_positions = {
        xss_planet: {"geocentric_longitude": 45.0}
    }

    svg_out = SVGChartEngine.generate_circular_zodiac_wheel(planetary_positions, title=xss_title)

    assert "<script>" not in svg_out
    assert "<img" not in svg_out
    assert "&lt;script&gt;" in svg_out
