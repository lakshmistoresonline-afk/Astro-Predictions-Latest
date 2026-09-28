# Phase 2E-R4 Cheshta Bala Validation

## Motion-Speed Classification
Cheshta Bala for star planets (Mars, Mercury, Jupiter, Venus, Saturn) is derived directly from geocentric daily velocity (`velocity_deg_day`):
- Vakra (Retrograde, `vel < 0`): 60 shashtiamsas
- Vikala (Stationary, `|vel| < 0.005`): 15 shashtiamsas
- Atichara / Chara (Fast, `vel > 1.15 * avg`): 45 shashtiamsas
- Sama (Normal, `0.85 * avg <= vel <= 1.15 * avg`): 30 shashtiamsas
- Manda (Slow, `0 < vel < 0.85 * avg`): 15 shashtiamsas

Luminaries:
- Sun: Cheshta = Ayana Bala
- Moon: Cheshta = Paksha Bala

Tested across direct, retrograde, fast velocity, and stationary boundary fixtures (`SHADBALA_FIXTURE_010` and `SHADBALA_FIXTURE_015`).
