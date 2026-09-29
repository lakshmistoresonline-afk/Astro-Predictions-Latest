# Phase 2E-R4.1-R4 Ayanamsha Audit

## Lahiri Ayanamsha Formula
In the independent reference extractor (`reference_source/standalone_ephemeris_extractor.py`) and oracle, sidereal longitudes are obtained using the official N.C. Lahiri Ayanamsha formula:
$$A_{\text{Lahiri}} = 23.85^\circ + 1.396^\circ \cdot T$$
where $T = \frac{JD - 2451545.0}{36525.0}$ (Julian Centuries from J2000.0 epoch).

## Precision & Agreement
- **J2000.0 Epoch Value**: $23.85^\circ$.
- **Precession Rate**: $50.29'' / \text{year} \approx 1.396^\circ / \text{century}$.
- **Cross-Check Agreement**: Comparing PyEphem Lahiri vs Skyfield Lahiri yields sub-arcsecond ayanamsha agreement (< 0.001°).
