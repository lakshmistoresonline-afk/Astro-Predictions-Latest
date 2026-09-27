# Astrovision Engine Audit

## 1. Astronomical Engine
- Calculates true solar, lunar, and planetary positions using Meeus rigorous ephemeris equations and perturbative terms.
- No synthetic offsets or fake latitude/longitude modifiers.

## 2. Vedic Engine
- Computes sidereal longitudes using Lahiri ayanamsha.
- Determines exact Nakshatra (1 to 27) and Pada (1 to 4) with boundary precision.
- Maps planetary dignities (Exaltation, Debilitation, Own Sign, Moolatrikona).

## 3. Dasha Engine
- Calculates Vimshottari Mahadasha sequence based on exact Moon longitude and elapsed nakshatra fraction.
- Fully supports 5-level micro-timing (Mahadasha down to Prana).
