# Phase 2E Initial Forensic Audit - Strength Engines

## 1. Existing Strength Calculations Discovered
The repository currently contains:
- `apps/api/engines/strength_engine.py`: Defines `StrengthEngine`.
  - Implements `calculate_shadbala()` and `calculate_ashtakavarga()`.

## 2. Synthetic Arithmetic Review
Looking at `apps/api/engines/strength_engine.py`:
- **Shadbala**: Uses synthetic math like `sthanabala = round(1.2 * mult + (lon % 10) * 0.02, 2)`, `digbala = round(0.9 * mult + (lon % 7) * 0.01, 2)`. This is entirely synthetic and not based on actual astrological rules.
- **Ashtakavarga**: Uses synthetic math: `b = 22 + int((sun_lon + moon_lon + idx * 13) % 15)`. This is entirely fabricated and not a true BAV/SAV calculation.

## 3. Legacy Consumer Paths
- `apps/api/engines/report_engine.py` consumes `StrengthEngine.calculate_shadbala()` and `StrengthEngine.calculate_ashtakavarga()` passing the legacy `planetary_positions` (which we adapted in Phase 2D-R4 to be built from `CanonicalVedicChart`).

## 4. Next Steps
The goal is to build an authoritative deterministic engine package (`apps/api/engines/strength/`) that properly computes BAV/SAV and the 6 Shadbala components directly from the `CanonicalVedicChart` state, without hard-coded synthetic mathematics. We will isolate the old logic and replace it with proper rule evaluations.
