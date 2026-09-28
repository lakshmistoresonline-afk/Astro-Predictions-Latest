# Phase 2E-R4 Drik Bala Validation

## BPHS Drishti Pinda Aspectual Strength
Evaluates exact angular distance between aspecting planet and target planet:
- 30°-60°: `(dist - 30) * 0.5`
- 60°-90°: `(dist - 60) + 15`
- 90°-120°: `(120 - dist) * 1.5`
- 150°-180°: `(dist - 150) * 2.0` (Max 60 at 180°)
- 180°-300°: `(300 - dist) / 2.0`

Special Aspects:
- Mars: 4th (90°-120°) & 8th (210°-240°) = +15 shashtiamsas
- Jupiter: 5th (120°-150°) & 9th (240°-270°) = +30 shashtiamsas
- Saturn: 3rd (60°-90°) & 10th (270°-300°) = +45 shashtiamsas

Benefic aspects add `+1/4th` of Drishti value; Malefic aspects subtract `-1/4th`.
