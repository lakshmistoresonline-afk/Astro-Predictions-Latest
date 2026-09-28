# Phase 2E-R3 Rule Inventory & Component Counting Definition

## 1. Major Balas (6 Balas)
1. **Sthana Bala** (Positional Strength)
2. **Dig Bala** (Directional Strength)
3. **Kala Bala** (Temporal Strength)
4. **Cheshta Bala** (Motional Strength)
5. **Naisargika Bala** (Natural Strength)
6. **Drik Bala** (Aspectual Strength)

## 2. Granular Subcomponent Inventory (16 Subcomponents Total)

### Sthana Bala Subcomponents (5 Subcomponents)
1. **Uccha Bala**: Exaltation/Debilitation angular distance (`(180 - min_dist) / 180 * 60`).
2. **Sapta Vargaja Bala**: Panchadha Maitri score evaluated across 7 Vargas (D1, D2, D3, D7, D9, D12, D30).
3. **Ojha-Yugma Bala**: Rashi & Navamsa odd/even sign gender alignment score.
4. **Kendradi Bala**: House placement score relative to Ascendant (Kendra=60, Panaphara=30, Apoklima=15).
5. **Drekkana Bala**: Gender-drekkana partition match score (15 shashtiamsas).

### Dig Bala Subcomponent (1 Subcomponent)
6. **Dig Bala**: Linear angular interpolation from cardinal power points (MC/Asc/Desc/IC).

### Kala Bala Subcomponents (8 Subcomponents)
7. **Nathonnatha Bala**: Diurnal/Nocturnal time-of-day solar distance to Nadir (IC).
8. **Paksha Bala**: Lunar phase Sun-Moon separation angle.
9. **Ayana Bala**: Declination-based strength derived from tropical longitude.
10. **Tribhaga Bala**: 1/3rd day/night partition lord strength (Jupiter gets 60 always).
11. **Vara Bala**: Day Lord (Vara) strength (+45 shashtiamsas).
12. **Hora Bala**: Hour Lord (Hora) strength (+60 shashtiamsas).
13. **Masa Bala**: Month Lord (Masa) strength (+30 shashtiamsas).
14. **Varsha Bala**: Year Lord (Varsha) strength (+15 shashtiamsas).

### Cheshta Bala Subcomponent (1 Subcomponent)
15. **Cheshta Bala**: Motion-speed classification (Vakra=60, Vikala=15, Atichara=45, Sama=30, Manda=15) derived from Phase 2A geocentric velocity `velocity_deg_day`. (Luminaries: Sun=Ayana, Moon=Paksha).

### Naisargika Bala Subcomponent (1 Subcomponent)
16. **Naisargika Bala**: Fixed classical BPHS natural strength constants.

### Drik Bala Subcomponent (1 Subcomponent)
17. **Drik Bala**: Full BPHS Drishti Pinda calculation from all aspecting planets including special aspects for Mars, Jupiter, Saturn.

## 3. Counting Summary
- **6 Major Balas**: Sthana, Dig, Kala, Cheshta, Naisargika, Drik.
- **16 Subcomponents**: Uccha, Sapta Vargaja, Ojha Yugma, Kendradi, Drekkana, Dig, Nathonnatha, Paksha, Ayana, Tribhaga, Vara, Hora, Masa, Varsha, Cheshta, Naisargika, Drik.
- **7 Classical Planets Evaluated**: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn.
