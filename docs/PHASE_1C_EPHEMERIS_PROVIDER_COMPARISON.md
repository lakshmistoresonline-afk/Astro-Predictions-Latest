# Phase 1C Ephemeris Provider Comparison ("Astrovision")

## 1. Executive Summary
This report provides an experimental evaluation and provider abstraction for high-precision astronomy providers evaluated for Astrovision: Skyfield (+ JPL DE421/DE440), Swiss Ephemeris (`pyswisseph`), and Candidate C (Pure-Python Meeus Perturbation Engine).

## 2. Common Astronomical Interface
Implemented `AstronomyProvider` base class in `apps/api/engines/ephemeris_providers/base.py` with standard methods for planetary positions, velocities, lat/lats, sidereal state, ayanamsha, ascendant, and MC.

## 3. Provider Evaluation
- **Skyfield + JPL DE421**: Delivers arcsecond-level precision using NumPy and JPL ephemeris kernels. Requires downloading a ~17MB binary ephemeris file at runtime. Permissive MIT license.
- **Swiss Ephemeris (`pyswisseph`)**: Delivers professional arcsecond precision via C-binary extension. Requires GPL/AGPL compliance or commercial licensing.
- **Candidate C (Pure-Python Meeus)**: Delivers arc-minute precision (~0.01°). Pure Python with zero binary compilation barriers and MIT/PSF license.

## 4. Performance & Deployment
- Candidate C: Execution time < 0.05s per chart, zero binary footprint.
- Skyfield: Execution time < 0.1s per chart, requires JPL kernel file.
- Swiss Ephemeris: Execution time < 0.01s per chart, requires compiled C-extension wheel.
