# Ephemeris Benchmark Plan ("Astrovision")

## 1. Objective
Define the exact independent numerical validation plan to benchmark candidate ephemeris engines against authoritative reference fixtures (including the Subramanian T S reference chart: 1986-09-28 16:30 IST, Palakkad).

## 2. Test Vectors & Target Dates
- **Historical Date**: 1986-09-28 11:00 UTC (Subramanian T S reference chart).
- **Modern Date**: 2026-09-27 12:00 UTC.
- **Equinox/Solstice Cases**: 2000-03-20, 2000-06-21.

## 3. Tolerances & Metrics
- Planetary Longitude: $\pm 0.01^\circ$ (for pure-Python Meeus) or $\pm 0.0001^\circ$ (for Swiss Ephemeris / Skyfield).
- Planetary Latitude: $\pm 0.05^\circ$.
- Retrograde Status: Binary match (True/False).
- Ascendant: $\pm 0.1^\circ$.
- MC: $\pm 0.1^\circ$.
