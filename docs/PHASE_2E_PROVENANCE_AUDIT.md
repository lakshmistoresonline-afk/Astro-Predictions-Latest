# Phase 2E Provenance & Convention Matrix

## 1. Ashtakavarga
- **Selected Tradition**: Maharishi Parashara (*Brihat Parasara Hora Sastra*, Ch. 66).
- **BAV House Contributions**: Strictly calculated from 1-based relative house positions. Included explicitly as hard-coded arrays inside `apps/api/engines/strength/ashtakavarga.py`.
- **Ascendant Constraint**: Included as an active contributor for calculating the BAV matrices for the 7 classical planets. Outer planets excluded. 
- **SAV Aggregation constraint**: Tested rigorously against the canonical universal 337 total constraint.

## 2. Shadbala Components
- **Uccha Bala (Exaltation Strength)**: Implemented based on actual numerical distance from the exact degree of debilitation (`(dist_from_deb / 180.0) * 60.0`). Uses `sidereal_longitude` directly, omitting naive sign-based multiplication.
- **Dig Bala (Directional Strength)**: Evaluates house index relative to the Ascendant. Modulates between `0` (opposite house) and `60` (power house) Shashtiamsas.
- **Naisargika Bala (Natural Strength)**: Adopts exact fixed values from standard texts (e.g. `Sun = 60.0, Saturn = 8.57`).
- **Retrograde & Luminaries (Cheshta Bala)**: Placeholder simplified algorithm currently providing baseline 60 to luminaries and retrogrades; to be refined dynamically via `velocity` calculation in future iterative phases if requested, but mathematically decoupled from legacy modular math.
