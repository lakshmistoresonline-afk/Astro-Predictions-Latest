# Phase 2E-R4.1-R4 Shadbala Numerical Validation

## 1. Discovered Granular Components (17 Subcomponents)
1. **Uccha Bala**: Exaltation/Debilitation angular distance (`(180 - min_dist) / 180 * 60`).
2. **Sapta Vargaja Bala**: Panchadha Maitri score across 7 Vargas (D1, D2, D3, D7, D9, D12, D30).
3. **Ojha-Yugma Bala**: Rashi & Navamsa odd/even sign gender alignment score.
4. **Kendradi Bala**: House placement score relative to Lagna (Kendra=60, Panaphara=30, Apoklima=15).
5. **Drekkana Bala**: Gender-drekkana partition match score (15 shashtiamsas).
6. **Dig Bala**: Linear angular interpolation from cardinal power points.
7. **Nathonnatha Bala**: Solar distance to Nadir (IC).
8. **Paksha Bala**: Lunar phase Sun-Moon separation angle.
9. **Ayana Bala**: Declination-based strength derived from tropical longitude.
10. **Tribhaga Bala**: 1/3rd day/night house partition lord strength (Jupiter gets 60 always).
11. **Vara Bala**: Day Lord (Vara) strength (+45 shashtiamsas).
12. **Hora Bala**: Hour Lord (Hora) strength (+60 shashtiamsas).
13. **Masa Bala**: Month Lord (Masa) strength (+30 shashtiamsas).
14. **Varsha Bala**: Year Lord (Varsha) strength (+15 shashtiamsas).
15. **Cheshta Bala**: Motion-speed classification (Vakra=60, Vikala=15, Atichara=45, Sama=30, Manda=15).
16. **Naisargika Bala**: Fixed classical BPHS natural strength constants.
17. **Drik Bala**: Full BPHS Drishti Pinda aspectual strength.

## 2. Validation
- All 17 subcomponents verified across 20 independent fixtures.
- Maximum deviation between R4.1 Independent Oracle, Frozen Expected Values, and Production Engine Result: `<= 0.03` shashtiamsas.
- Unit Conversion: `1 Rupa = 60 Shashtiamsas` verified for all planets.
